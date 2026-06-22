# Publication strategy

Last updated: 2026-06-22

## 1. Strategy summary

- **Working title:** *A reproducible re-measurement of the Voynich Manuscript's statistical structure, with a systematic cross-section label/crib survey.*
- **Honest positioning:** **NOT** a decipherment and **NOT** a discovery paper. It is a *reproducible-replication + systematic-survey + negative-results* contribution. Most core statistics replicate established work (Tiltman 1967; Currier 1976; Reddy & Knight 2011; Montemurro & Zanette 2013; Timm & Schinner 2020; Bowern & Lindemann 2021).
- **Novel core (what carries the paper):** (1) exhaustive, openly-released cross-section label/crib survey; (2) position-dependent (slot) cipher null result; (3) an open finite-state generator + EVA renderer with precision/recall validation; (4) timely test against Greshko (2025) Naibbe cipher.
- **Venue path:** **A → PLOS ONE** (soundness-not-novelty; best home for rigorous replication/negative results), **B → Cryptologia** (methods/survey bar; engage prior corpus), **C → CEUR-WS Voynich workshop** (short-form/priority). Info-theoretic reframing → *Entropy*; quantitative-linguistic → *Glottometrics*.
- **Acceptance odds (honest):** as-is, ~0%. After the four blockers fixed, ~50–60% at PLOS ONE / CEUR-WS, ~30–40% at Cryptologia.

## 2. Pre-submission readiness (traffic light)

| Item | State |
|---|---|
| Reproducible code + data | 🟡 scripts present; no env pin, no checksums, non-deterministic cipher search |
| Uncertainty quantification (CIs, tests) | 🔴 started (h₂ CIs only); must cover all metrics |
| Transcription robustness (EVA/v101/Cuva; ≥2 transcribers) | 🔴 not started — **the gating blocker** |
| Size-matched, multi-text comparison corpora | 🔴 single-text per language; Arabic too small |
| Literature review + references.bib + novelty table | 🟡 references.bib done; related-work section + per-result novelty table not yet in manuscript |
| Overclaims corrected (audit C1–C5 propagated) | 🔴 not yet in main.md |
| Numeric inconsistencies reconciled | 🔴 Zipf slope, grammar order, label counts |
| Iconography verified vs high-res scans | 🔴 rests on low-res facsimile + vision agents; archive.org high-res now available to verify |
| Manuscript prose (APA, hedged, de-AI) | 🟡 honest but needs reframe |
| Word + PDF + 600-DPI figures | 🟢 build pipeline exists |

**Green ≈ 1/10. Not submittable.**

## 3. Acceptance-readiness rubric (target ≥80% green, 0 blockers)

| Dimension | Weight | Now |
|---|---|---|
| Novelty / positioning honesty | 15% | 🔴→fixable |
| Statistical rigor (CIs, tests, corrections) | 25% | 🔴 |
| Robustness (transcription/transcriber) | 20% | 🔴 |
| Reproducibility (env, checksums, determinism) | 15% | 🟡 |
| Literature grounding | 10% | 🟡 |
| Writing / honesty / hedging | 10% | 🟡 |
| Figures / package completeness | 5% | 🟢 |

Composite readiness ≈ **25%**. Blockers present.

## 4. Path to submittable (ordered)

1. **Transcription robustness** — re-run h₂, slot grammar, finite-state precision/recall on EVA + v101/Cuva and Takahashi + Zandbergen; report bootstrap CIs. *(Needs the alternative transcription files.)*
2. **Uncertainty quantification everywhere** — extend `harden_stats.py` to word-order info, slot rates, crib Jaccards, generator precision/recall; permutation tests for the one-edit ladder and LAAFU; Holm correction across the battery.
3. **Related-work section + per-result novelty table** ("replicates X" vs "new") using `references.bib`.
4. **Propagate audit C1–C5** into the manuscript; reconcile the numeric inconsistencies; replace the time-capped cipher search with fixed-iteration multi-restart + CI.
5. **Size-matched multi-text corpora**; drop or expand Arabic.
6. **Verify iconography** against the archive.org high-resolution facsimile; give real citations for the merlon/map claims or demote them.

## 5. Lessons learned (append-only)

- 2026-06-22: A hostile review surfaced that the project replicates far more than it discovers; the supplementary `AUDIT_LOG.md` already retracted claims the manuscript still shipped. Core lesson: a literature/novelty check belongs *before* writing, per standing doctrine — it was run late and reframed the entire contribution.
