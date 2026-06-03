# AskPeer — Product Plan

> Last updated: 2026-06-03
> Status: Design phase

---

## 1. Product Thesis

**Academia has no "quick expert call" culture.** In industry, you pay $500 for a 30-minute call with an expert. In academia, your only option is cold-emailing paper authors or begging your PI's network. This is absurd — academia has *more* experts per capita than any industry, yet less efficient knowledge exchange.

**The bet**: If you make expert matching frictionless and incentive-aligned, researchers will use it. The demand is latent. The supply is abundant (retired PIs, industrial scientists, researchers between grants, postdocs with niche skills).

---

## 2. Target Users

### Demand Side (Seekers)
- PhD students stuck on methods
- PIs entering a new subfield
- Researchers needing statistical/methodological validation
- Cross-disciplinary projects needing translation

### Supply Side (Experts)
- Retired/emeritus professors (time + wisdom)
- Industry scientists (want academic engagement)
- Postdocs with niche technical skills
- Researchers between grants (income + relevance)

---

## 3. MVP Scope

### In Scope
- [ ] LLM-based expertise extraction from papers/CV
- [ ] Question → domain classification
- [ ] Vector similarity matching (expertise embeddings)
- [ ] Minimal web UI: question input + results display
- [ ] Email introduction (platform hands off)
- [ ] 10 expert profiles seeded manually

### Out of Scope (v1)
- [ ] Payment / billing
- [ ] Platform calls (Zoom integration)
- [ ] User auth / accounts
- [ ] Rating / reputation system
- [ ] Automated expert onboarding
- [ ] Mobile app

### Why This Scope
The riskiest assumption is: **will researchers actually use this?** Everything else (payment, auth, platform calls) is execution risk, not product risk. MVP tests the core hypothesis with minimum build.

---

## 4. Technical Architecture (MVP)

```
┌──────────────────────────────────────────────────┐
│                   AskPeer MVP                     │
├──────────────┬───────────────────────────────────┤
│   Frontend   │  Streamlit (single-page)           │
├──────────────┼───────────────────────────────────┤
│   Backend    │  Python FastAPI                    │
├──────────────┼───────────────────────────────────┤
│   Matching   │  Sentence-transformers embeddings  │
│              │  + cosine similarity               │
├──────────────┼───────────────────────────────────┤
│   Expertise  │  LLM (DeepSeek/OpenRouter)         │
│   Extraction │  papers → structured profile       │
├──────────────┼───────────────────────────────────┤
│   Storage    │  SQLite (experts + questions)      │
├──────────────┼───────────────────────────────────┤
│   Delivery   │  SMTP email intro                  │
└──────────────┴───────────────────────────────────┘
```

### Expertise Graph Schema
```json
{
  "expert_id": "exp_001",
  "name": "Dr. Jane Smith",
  "domains": ["cryo-EM", "membrane proteins", "structural biology"],
  "methods": ["single-particle analysis", "tomography", "FIB-SEM"],
  "techniques": ["grid preparation", "data processing", "RELION"],
  "publications": 45,
  "h_index": 28,
  "availability": "2-3 calls/week",
  "delivery_modes": ["call", "async"],
  "rate": null,
  "embedding": [0.123, -0.456, ...]
}
```

### Question Schema
```json
{
  "question_id": "q_001",
  "text": "I'm trying to solve a cryo-EM structure of a ~50kDa membrane protein but getting severe preferred orientation. Tried grid screening and detergent exchange — no luck. What am I missing?",
  "domain": "structural biology",
  "method": "cryo-EM",
  "technique": "grid preparation",
  "depth": "troubleshooting",
  "embedding": [0.234, -0.567, ...]
}
```

---

## 5. Expert Seeding Strategy

For MVP, manually curate 10 experts:
- 3 from personal academic network
- 3 from papers the team has read/cited
- 4 from publicly available profiles (Google Scholar, institutional pages)

Each expert gets:
1. Papers ingested → LLM extracts expertise tags
2. Manual review of extracted tags
3. Embedding computed
4. Profile stored

---

## 6. Matching Algorithm

```
1. User submits question
2. LLM classifies: domain, method, technique, depth
3. Generate question embedding
4. Cosine similarity against all expert embeddings
5. Return top 3 with similarity scores
6. (Optional) re-rank with LLM: "Would expert X be good for question Y?"
```

---

## 7. Delivery Flow

```
Match found → Researcher clicks "Connect"
  → Pre-written intro email generated
  → Sent to expert: "Dr. Smith, a researcher working on [topic]
    is seeking your expertise on [specific problem].
    Would you be available for a 30-min call or async feedback?"
  → Expert replies → Platform CC's researcher
  → Both parties take it from there
```

Platform's job ends at the intro. No call hosting, no payment processing, no dispute resolution.

---

## 8. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Researchers won't pay | Product fails | Start with pro-bono / reciprocity model |
| Experts won't sign up | Network effect fails | Seed with personal network + show usage stats |
| LLM expertise extraction inaccurate | Bad matches | Manual review in MVP; iterate prompt |
| Cold-start: no experts | Can't demo | Pre-load 10 expert profiles |
| Academic culture resistant | Slow adoption | Target early-adopter subfields (AI/ML, comp bio) |

---

## 9. Success Metrics (MVP)

- **10 expert profiles** created
- **1 real match** made (question → expert → conversation)
- **Qualitative feedback**: would researcher use again? would expert take more calls?

---

## 10. Post-MVP Roadmap

### v0.2 — "Actually Useful"
- User accounts (email + Google Scholar link)
- Expert self-onboarding (upload papers → auto-profile)
- Question history + re-ask

### v0.3 — "Network Effects"
- Rating system (was this expert helpful?)
- Expert discovery (browse by domain)
- Institution-based trust (verified .edu emails)

### v1.0 — "Business Model"
- Payment processing (Stripe)
- Platform calls (Zoom API)
- Expert revenue dashboard
- Institution subscription plans

---

## 11. Competition & Positioning

| Competitor | What They Do | AskPeer Difference |
|------------|-------------|-------------------|
| Ethos | Industry expert calls, $500/hr | Academic focus, flexible incentives |
| Kolabtree | Freelance scientists for hire | Focused on quick consults, not projects |
| ResearchGate Q&A | Free forum questions | Guaranteed expert response, not hope |
| Traditional peer review | Unpaid, 6-month turnaround | Not review — consultation |
| Cold emailing | Free, low response rate | AI-matched, higher conversion |

---

## 12. Open Questions

1. **Incentive model**: credit-based reciprocity vs. paid vs. hybrid?
2. **Verification**: how to prevent fake experts without heavy manual review?
3. **Liability**: what if bad advice leads to wasted experiments?
4. **Scale**: at what point does manual curation break?

---

*Build the smallest thing that proves someone will say "thank god this exists."*
