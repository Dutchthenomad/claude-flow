"""LangChain-powered hybrid retrieval (dense + lexical + optional rerank).

This module is intentionally optional: it only activates when LangChain deps exist.
Enable via:
  - env: `CLAUDE_FLOW_RAG_BACKEND=langchain_hybrid`
  - or by passing `backend="langchain_hybrid"` to `retrieval.retrieve.search()`.
"""

from __future__ import annotations

import math
import os
import re
from dataclasses import dataclass
from typing import Any


def is_available() -> bool:
    """Return True if required LangChain modules can be imported."""
    try:
        import langchain_core  # noqa: F401
        import langchain_classic  # noqa: F401
    except Exception:
        return False
    return True


def _ensure_langchain() -> None:
    if not is_available():
        raise RuntimeError(
            "LangChain backend requested but dependencies are missing.\n"
            "Install in the rag-pipeline venv, e.g.:\n"
            "  rag-pipeline/.venv/bin/pip install -r rag-pipeline/requirements-langchain.txt\n"
            "Or editable installs from your local checkout:\n"
            "  rag-pipeline/.venv/bin/pip install -e /home/nomad/Desktop/LANGCHAIN/libs/core "
            "-e /home/nomad/Desktop/LANGCHAIN/libs/text-splitters "
            "-e /home/nomad/Desktop/LANGCHAIN/libs/langchain"
        )


_TOKEN_RE = re.compile(r"[A-Za-z0-9_./-]+")


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


@dataclass(frozen=True)
class _BM25Config:
    k1: float = 1.5
    b: float = 0.75


class _BM25Index:
    def __init__(self, docs: list[dict[str, Any]], config: _BM25Config | None = None):
        self._docs = docs
        self._config = config or _BM25Config()

        self._doc_tokens: list[list[str]] = []
        self._doc_tf: list[dict[str, int]] = []
        self._doc_len: list[int] = []
        self._df: dict[str, int] = {}

        for doc in docs:
            tokens = _tokenize(doc["text"])
            self._doc_tokens.append(tokens)
            tf: dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            self._doc_tf.append(tf)
            self._doc_len.append(len(tokens))

            for term in tf.keys():
                self._df[term] = self._df.get(term, 0) + 1

        self._n_docs = len(docs)
        self._avgdl = (sum(self._doc_len) / self._n_docs) if self._n_docs else 0.0

    def score(self, query: str) -> list[float]:
        tokens = _tokenize(query)
        if not tokens or self._n_docs == 0:
            return [0.0] * self._n_docs

        k1 = self._config.k1
        b = self._config.b
        scores = [0.0] * self._n_docs

        for term in tokens:
            df = self._df.get(term, 0)
            if df == 0:
                continue

            # BM25 idf with smoothing
            idf = math.log((self._n_docs - df + 0.5) / (df + 0.5) + 1.0)

            for i in range(self._n_docs):
                tf = self._doc_tf[i].get(term, 0)
                if tf == 0:
                    continue

                dl = self._doc_len[i]
                denom = tf + k1 * (1.0 - b + b * (dl / (self._avgdl or 1.0)))
                scores[i] += idf * (tf * (k1 + 1.0)) / (denom or 1.0)

        return scores


_bm25_index: _BM25Index | None = None
_bm25_doc_count: int | None = None


def _get_bm25_index() -> _BM25Index:
    global _bm25_index, _bm25_doc_count

    from storage.store import count, get_all_documents

    current_count = count()
    if _bm25_index is not None and _bm25_doc_count == current_count:
        return _bm25_index

    docs = get_all_documents()
    _bm25_index = _BM25Index(docs)
    _bm25_doc_count = current_count
    return _bm25_index


class _SentenceTransformersCrossEncoder:
    def __init__(self, model_name: str):
        from sentence_transformers import CrossEncoder

        self._model = CrossEncoder(model_name)

    def score(self, text_pairs: list[tuple[str, str]]) -> list[float]:
        # sentence-transformers CrossEncoder returns list/np.ndarray of floats
        preds = self._model.predict(text_pairs)
        return [float(x) for x in preds]


_cross_encoder: _SentenceTransformersCrossEncoder | None = None
_cross_encoder_name: str | None = None


def _get_cross_encoder() -> _SentenceTransformersCrossEncoder | None:
    """Best-effort cross-encoder loader; returns None if not loadable."""
    global _cross_encoder, _cross_encoder_name

    model_name = os.getenv(
        "CLAUDE_FLOW_CROSS_ENCODER_MODEL",
        "cross-encoder/ms-marco-MiniLM-L-6-v2",
    )
    if _cross_encoder is not None and _cross_encoder_name == model_name:
        return _cross_encoder

    try:
        _cross_encoder = _SentenceTransformersCrossEncoder(model_name)
        _cross_encoder_name = model_name
        return _cross_encoder
    except Exception:
        return None


def _doc_to_result(doc: Any, score: float) -> dict[str, Any]:
    meta = getattr(doc, "metadata", {}) or {}
    return {
        "id": meta.get("id"),
        "text": getattr(doc, "page_content", ""),
        "source": meta.get("source", ""),
        "line_start": meta.get("line_start", 0),
        "line_end": meta.get("line_end", 0),
        "headers": meta.get("headers", []),
        "score": float(score),
    }


def search(
    query_text: str,
    top_k: int = 5,
    *,
    dense_k: int | None = None,
    lexical_k: int | None = None,
    candidate_k: int | None = None,
    weights: tuple[float, float] = (0.75, 0.25),
    rerank: bool | None = None,
) -> list[dict[str, Any]]:
    """Hybrid search using LangChain's retriever interfaces + ensemble ranking.

    Returns the same dict format as `retrieval.retrieve.search()`.
    """
    _ensure_langchain()

    from langchain_core.callbacks import CallbackManagerForRetrieverRun
    from langchain_core.documents import Document
    from langchain_core.retrievers import BaseRetriever
    from langchain_classic.retrievers.ensemble import EnsembleRetriever

    from embeddings.embedder import embed_text
    from storage.store import query as chroma_query

    dense_k = dense_k or max(top_k * 4, 20)
    lexical_k = lexical_k or max(top_k * 4, 20)
    candidate_k = candidate_k or max(top_k * 6, 40)
    if rerank is None:
        rerank = os.getenv("CLAUDE_FLOW_RAG_RERANK", "1").strip() not in ("0", "false", "False")

    class DenseRetriever(BaseRetriever):
        k: int

        def _get_relevant_documents(
            self,
            query: str,
            *,
            run_manager: CallbackManagerForRetrieverRun,
        ) -> list[Document]:
            emb = embed_text(query)
            results = chroma_query(emb, top_k=self.k)
            docs: list[Document] = []
            for r in results:
                docs.append(
                    Document(
                        page_content=r["text"],
                        metadata={
                            "id": r.get("id") or f"{r['source']}:{r['line_start']}:{r['line_end']}",
                            "source": r["source"],
                            "line_start": r["line_start"],
                            "line_end": r["line_end"],
                            "headers": r.get("headers", []),
                            "dense_score": r.get("score", 0.0),
                            "retriever": "dense",
                        },
                    )
                )
            return docs

    class LexicalRetriever(BaseRetriever):
        k: int

        def _get_relevant_documents(
            self,
            query: str,
            *,
            run_manager: CallbackManagerForRetrieverRun,
        ) -> list[Document]:
            idx = _get_bm25_index()
            scores = idx.score(query)
            scored = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

            docs: list[Document] = []
            for doc_i, s in scored[: self.k]:
                d = idx._docs[doc_i]
                docs.append(
                    Document(
                        page_content=d["text"],
                        metadata={
                            "id": d.get("id") or f"{d['source']}:{d['line_start']}:{d['line_end']}",
                            "source": d["source"],
                            "line_start": d["line_start"],
                            "line_end": d["line_end"],
                            "headers": d.get("headers", []),
                            "bm25_score": float(s),
                            "retriever": "lexical",
                        },
                    )
                )
            return docs

    ensemble = EnsembleRetriever(
        retrievers=[DenseRetriever(k=dense_k), LexicalRetriever(k=lexical_k)],
        weights=[weights[0], weights[1]],
        id_key="id",
    )

    candidates = ensemble.invoke(query_text)
    candidates = candidates[:candidate_k]

    # Default score uses dense_score if present (or bm25_score), unless rerank replaces it.
    base_scores: list[float] = []
    for d in candidates:
        meta = d.metadata or {}
        base_scores.append(float(meta.get("dense_score") or meta.get("bm25_score") or 0.0))

    if rerank and candidates:
        cross_encoder = _get_cross_encoder()
        if cross_encoder is not None:
            try:
                rerank_scores = cross_encoder.score(
                    [(query_text, d.page_content) for d in candidates]
                )
                ranked = sorted(
                    zip(candidates, rerank_scores, strict=False),
                    key=lambda x: x[1],
                    reverse=True,
                )
                final_docs = [d for d, _ in ranked[:top_k]]
                final_scores = [s for _, s in ranked[:top_k]]
                return [_doc_to_result(d, s) for d, s in zip(final_docs, final_scores, strict=False)]
            except Exception:
                # Fall back to base ordering below
                pass

    final_docs = candidates[:top_k]
    final_scores = base_scores[:top_k]
    return [_doc_to_result(d, s) for d, s in zip(final_docs, final_scores, strict=False)]
