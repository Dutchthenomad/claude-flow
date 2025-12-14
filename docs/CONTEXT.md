# Docs - Agent Context

## Purpose
This folder contains **human-readable documentation** and methodology guides. These docs serve both humans and agents as reference material.

## Contents
| Path | Description |
|------|-------------|
| `WORKFLOW_QUICKREF.md` | Quick reference for the complete workflow |
| `methodology/` | Detailed methodology documentation |
| `architecture/` | System architecture documentation |

## Integration Points
- Docs can be imported into CLAUDE.md via `@docs/filename.md`
- Docs are indexed for RAG retrieval (future)
- Docs inform agent behavior via context loading

## Development Status
- [x] Initial structure
- [x] WORKFLOW_QUICKREF migrated
- [ ] Methodology docs
- [ ] Architecture docs
- [ ] Production ready

## For Future Agents
When writing documentation:
1. Use clear, concise language
2. Include practical examples
3. Keep docs up-to-date with code changes
4. Use markdown formatting consistently
5. Cross-reference related docs
6. Consider both human and agent readers
