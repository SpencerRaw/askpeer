> 🌐 [中文文档](README.zh-CN.md) | **English**

# 🧠 AskPeer — On-Demand Academic Expert Network

> **Got a research problem? Ask a peer who's solved it before.**

AskPeer connects researchers with domain experts for on-demand consultation. Not peer review. Not co-authorship negotiation. Just: *you have a problem → we find the person who knows the answer → you talk.*

---

## Why

Three things broke in academic knowledge exchange:

| Broken Thing | How It Works Now | AskPeer |
|---|---|---|
| **Peer review** | 3-6 months, unpaid, random quality | Not our problem. We do consultation. |
| **Methodology help** | Cold-email a paper author, hope they reply | AI matches you to the right person in hours |
| **Cross-domain expertise** | Your PI's network. That's it. | Global expertise graph, no gatekeepers |

The a16z-backed [Ethos](https://askethos.com) proved this model works for industry ($500/hr expert calls). AskPeer brings it to academia — with academic-appropriate incentives, not just cash.

---

## What AskPeer Is

```
Researcher has a question
        │
        ▼
   AI analyzes question
   + searches expertise graph
        │
        ▼
   Top 3 expert matches
        │
        ▼
   Researcher picks one
        │
        ▼
   30-min consultation
   (call / async / in-person)
        │
        ▼
   Problem solved. Rate & thank.
```

**Delivery modes** — flexible, not just paid calls:
- 🎥 **Live call** — 30min Zoom / video
- ✍️ **Async feedback** — written response within 48h
- 🤝 **Collaboration** — if both sides want, turn into co-authorship

**Incentives** — academic-appropriate:
- Experts set their own rates (or pro-bono)
- Institutional credit / departmental recognition
- Co-authorship opt-in (if consultation leads to collaboration)

---

## MVP — Phase 1

Minimal matching engine. No payment. No auth wall.

```
┌─────────────────────────────────────────┐
│  AskPeer MVP                            │
│                                         │
│  [ Describe your research problem...  ] │
│  [ Your field: _______ ]               │
│  [ Preferred mode: call / async / any ] │
│                                         │
│         [ Find an Expert ]              │
│                                         │
│  ── Results ──────────────────────────  │
│  Dr. A — cryo-EM, membrane proteins     │
│  Dr. B — MD simulation, force fields    │
│  Dr. C — statistical analysis, R        │
│                                         │
│  [ Connect with Dr. A ]                 │
└─────────────────────────────────────────┘
```

MVP delivers: **problem → match → intro email.** No platform calls, no payment — just connect two researchers.

---

## Technical Approach

| Layer | Technology |
|-------|-----------|
| Expertise extraction | LLM reads papers/CV → structured expertise graph |
| Question understanding | LLM classifies domain + method + depth |
| Matching | Vector similarity over expertise embeddings |
| Frontend | Minimal web UI (Streamlit or plain HTML) |
| Backend | Python + SQLite (MVP) |

---

## Comparison

| | Ethos (askethos.com) | AskPeer |
|---|---|---|
| Domain | Industry/business | Academic research |
| Users | Companies + consultants | Researchers + researchers |
| Price | $500/hr typical | Academic-appropriate (flexible) |
| Delivery | Paid calls only | Calls, async, collaboration |
| Vetting | AI voice interview | AI paper-analysis interview |
| Funding | a16z ($22.75M) | Bootstrapped / open-source |

---

## Development Status

- [x] Concept & design
- [ ] MVP: matching engine
- [ ] MVP: web UI
- [ ] Expert onboarding pipeline
- [ ] Pilot with 10 experts, 10 researchers

---

## Inspiration

- [Ethos](https://askethos.com) — AI expert network (a16z-backed)
- [SciDAO](https://github.com/SpencerRaw/sci-dao) — decentralized science
- The unbearable slowness of traditional peer review

---

## License

MIT
