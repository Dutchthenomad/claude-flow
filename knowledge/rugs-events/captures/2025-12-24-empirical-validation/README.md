# Empirical Validation Package: 2025-12-24

**Status:** Ready for Review and Ingestion
**Validation Tier:** VERIFIED (awaiting CANONICAL promotion)

---

## Summary

Captured 23,194 WebSocket events from 11 authenticated games on rugs.fun to:
1. Map action → confirmation events for BotActionInterface
2. Discover novel events/fields not in canonical spec
3. Measure latency distributions

---

## Key Discoveries

| Finding | Impact |
|---------|--------|
| Button clicks use HTTP, not WebSocket | Changes execution model |
| 10 novel events found | Spec update required |
| 22 undocumented fields in `playerUpdate` | Major spec expansion |
| Sidebet events (`currentSidebet`, `currentSidebetResult`) | Critical for bot |

---

## Package Contents

```
2025-12-24-empirical-validation/
├── README.md                          # This file
├── methodology/
│   └── COLLECTION_METHODOLOGY.md      # How data was collected
├── raw_captures/
│   └── full_game_capture_20251224_105411.jsonl  # 108MB raw data
└── analysis/
    ├── CAPTURE_ANALYSIS_2025-12-24.md  # Detailed event analysis
    ├── CAPTURE_ANALYSIS_SUMMARY.md     # Executive summary
    └── confirmation-mapping.md          # Action→Event mapping
```

---

## Ingestion Checklist

- [ ] Human review of novel events
- [ ] Approve CANONICAL promotion for key events
- [ ] Update `WEBSOCKET_EVENTS_SPEC.md`
- [ ] Run ChromaDB ingestion on analysis docs
- [ ] Move to permanent captures folder

---

## Quick Stats

| Metric | Value |
|--------|-------|
| Total Events | 23,194 |
| Unique Event Types | 19 |
| Games Observed | 11 |
| Duration | ~30 minutes |
| File Size | 108 MB |
| Novel Events | 10 |
| Novel Fields | 22 |

---

*Collected: December 24, 2025 by Claude Code + Dutch*
