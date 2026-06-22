# Godfather / super-audit review

Last updated: 2026-06-22

Two independent adversarial reviews — a literature-novelty check and a hostile methods/integrity audit — plus the standing self-audit. Verdict up front: **as a journal submission this is REJECT / major-revision. The science is honest, but it is not yet a publishable paper.** This document is the action list.

## Verdict in one paragraph

Most core results (low conditional entropy ≈2 bits/char; Currier A/B; prefix–core–suffix slot grammar; Zipf; binomial word length; finite-state/Markov reproducibility; label-vs-body differences) **replicate 25–50 years of established work** (Tiltman 1967; Currier 1976; Stolfi ~2000; Reddy & Knight 2011; Montemurro & Zanette 2013; Timm & Schinner 2020; Bowern & Lindemann 2021). They are not discoveries. The work is publishable **only** if reframed as (a) a fully reproducible open re-measurement, and/or (b) a **systematic cross-section label/crib survey** (the one genuinely under-published component), with proper statistics and a literature review.

## BLOCKERS (must fix before any submission)

1. **No inferential statistics.** Every headline number is a bare point estimate — no CIs, SEs, bootstrap, permutation tests, or effect sizes. *Status: STARTED* — bootstrap 95% CIs now computed for h₂ (Voynich 2.159 [2.141, 2.175] vs Latin 3.300 [3.291, 3.308]; non-overlapping ⇒ the gap is not sampling noise; `harden_stats.py`). Must extend to word-order info, slot-grammar rates, finite-state precision/recall, and all crib metrics.
2. **Single transcriber / single transcription.** Everything rests on Takahashi EVA (`LSI_ivtff_0d.txt`). Entropy, slot grammar, and the finite-state result all depend on glyph segmentation, which **differs across EVA / v101 / Cuva** and across transcribers (Takahashi / Zandbergen / Currier). *Unfixed.* Core stats must be re-run on ≥2 transcription systems and ≥2 transcribers with CIs. **This is the single most important fix.** If results survive transcription choice, the claims become defensible; if not, that is itself the finding.
3. **No literature review / no references.** Nearly every replicated result is uncredited; there is no `references.bib`. *Status: STARTED* — `references.bib` created with verified citations; a per-result novelty table ("replicates X" vs "new here") must go into the manuscript.
4. **Unmatched / inadequate comparison corpora.** Arabic ≈1.4k tokens is too small; comparators are single-text per language; `order_info` uses a non-random head-slice. Must use size-matched, randomly-sampled, multi-text corpora with within-language variance.

## MAJOR issues

- **Audit corrections not propagated into the manuscript.** `AUDIT_LOG.md` C1–C5 downgrade the line-as-unit effect (small; plausibly scribal decoration), the "iconography legible" framing, the combinatorial-imagery claim, the homophone count, and note the Naibbe match is by-construction — but `main.md` still ships the pre-correction wording. *Fix: propagate all five.*
- **Overclaims:** "iconography legible" → "interpretable/contextualizable"; "statistically indistinguishable" (§5) needs an actual equivalence/GOF test; "~18–22 primitives" implies a measurement that doesn't exist (vision-agent judgement) — hedge or quantify.
- **Weak null models / non-deterministic cipher search** (22 s wall-clock cap defeats the seed → hardware-dependent results). Replace with fixed-iteration, multi-restart search reporting convergence + CI.
- **No multiple-comparison correction** across the test battery.
- **Castle/merlon caveat laundered:** `rosettes_foldout.md` flags it honestly ("cited, not verified from this low-res facsimile"); `main.md` §1/§6 and `PROJECT_STATUS` treat Ghibelline-merlon dating as settled. *Fix: demote in main text, or verify against the high-res archive.org facsimile now available, with a real citation.*

## Numeric inconsistencies to reconcile (integrity-query triggers)

- Zipf slope: −1.01 (§4.1) vs −0.92/−0.91 (§5 table) — different rank cutoffs; state method, pick one.
- Grammar order: prose says "order-3"; distilled grammar shown is order-1; headline 94.2/89.6% must be tagged to a specific order.
- Word-order gap "0.14–0.16" (§4.4) vs line-as-unit residual "0.093" (audit) — distinct quantities, clarify.
- Zodiac label count 296 (`zodiac_crib`) vs 363 (`label_crib_all_sections`) — by-nymph vs all-loci; reconcile and state which feeds §6.

## Citation flags (from novelty check — do NOT ship without fixing)

- "Wastl & Feger 2018" UNVERIFIED — use their 2014 figshare item.
- Rugg 2004 title = "An Elegant Hoax? A Possible Solution to the Voynich Manuscript."
- Timm & Schinner cite as **2020**, *Cryptologia* 44(1).
- Greshko/Naibbe: online-first DOI only, no vol/issue.
- Bennett 1976 = entropy source only (not Zipf, not word-length).
- C14 1404–1438 has no peer-reviewed journal paper (U. Arizona announcement) — frame accordingly.
- Stolfi grammar/word-length and Vogt 2012 LAAFU are grey literature — tag as such; Reddy & Knight 2011 is the safe peer-reviewed anchor.

## What is genuinely novel (the publishable core)

1. **Systematic, exhaustive, reproducible cross-section label/crib survey** — not previously published in this form.
2. **Position-dependent (slot) cipher null result** — a specific refutation not in the prior generative-model literature.
3. **An explicit, openly-released finite-state generator + EVA-rendering tool** with precision/recall validation.
4. **Timely engagement with Greshko (2025) Naibbe** — testing it against re-measured statistics.

## Realistic venues

- **Cryptologia** (primary) — methods/survey bar; engage prior corpus or desk-reject.
- **PLOS ONE** (fallback) — soundness-not-novelty; best home for a rigorous replication / negative-results paper; strict on stats + open data/code.
- **CEUR-WS Voynich workshop** — priority/short-form.
- **Entropy (MDPI)** / **Glottometrics** — info-theoretic / quantitative-linguistic framing.

## Bottom line

Honest, careful, reproducible-in-spirit work that **currently replicates more than it discovers**. With (1) uncertainty quantification, (2) transcription-robustness, (3) a real related-work + novelty table, and (4) the cross-section crib survey as the centerpiece, it becomes a legitimate — if modest — contribution (best fit PLOS ONE or Cryptologia). Without those four, it is not submittable.
