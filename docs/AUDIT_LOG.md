# Audit log — adversarial self-review of experiments and interpretations

Last updated: 2026-06-22

This file records a deliberately hostile review of my own work on this project, in the spirit of "what would a skeptical reviewer kill us on?" Findings are kept even when they undercut earlier claims.

## A. Experiments — are the numbers sound?

| Experiment | Result | Verdict on soundness |
|---|---|---|
| Character entropy h₂ = 2.16 | reproducible, matches literature (Zandbergen, Bowern) | **Solid.** Independently confirmed; the h2 bug (negative value) was caught and fixed before reporting. |
| Multilingual sweep (8 langs) | VMS outlier on h₂ and word-order | **Solid**, but Arabic is a *small* sample (~1.4k words); flagged in the figure. Sanskrit/Finnish are full-size. |
| Reverse-engineered grammar | 94% precision, 90% recall, matched Zipf/length/h2 | **Solid and decisive.** Reproduces Stolfi / Timm & Schinner. |
| Line-as-unit (0.093 bits) | real 0.093 vs grammar 0.001 bits | **Numerically sound** (replicates Currier 1976). **Interpretation over-stated — see C1.** |
| Plaintext budget | ~10k words "fits" | **Weak by design — see C2.** A consistency check, not evidence. |
| Homophone clusters | ~8 families among top-120 words | **Qualitatively real, quantitatively soft — see C3.** |
| Illustration combinatoriality | "~18–22 primitives, combinatorial" | **Soft/subjective — see C4.** |

No computational errors found on re-review. The corrections below are about **interpretive weight**, not arithmetic.

## B. Track record on honesty (what went right)

- Caught and corrected a mislabelled "Latin" corpus (was an English translation) before reporting any result.
- Caught and fixed an impossible negative conditional-entropy value (context-counter bug).
- Discarded a slot-grammar coverage statistic that was trivially 100% by construction.
- Refused at every turn to fabricate a translation, and debunked three external decipherment claims rather than endorsing a satisfying story.

## C. Where I over-claimed, and the corrections

**C1 — The line-as-unit effect is weaker evidence than I repeatedly framed.**
Across several turns I treated the line-as-unit signal as "the hardest property for a cipher to explain" and "the frontier of the mystery." Two corrections: (i) its **magnitude is small** — 0.093 bits/word about a word's first glyph; (ii) the dominant component (flamboyant gallows on line-initial words) is **plausibly scribal decoration** — enlarged/ornamented first letters, exactly as medieval scribes routinely drew, and exactly the mechanism (nulls / decorative `<p>`) that Greshko (2025) invokes. If it is decoration, it is **cosmetic, not information-bearing**, and is weakly diagnostic between "cipher" and "construct." **Net: downgrade this from strong evidence to suggestive.**

**C2 — The plaintext-budget result is not evidence for the cipher hypothesis.**
It shows only that a ~10k-word message *could* fit under the ciphertext at a plausible verbosity. Almost any verbose scheme can be made to "balance" by choosing the verbosity factor. It rules out a gross impossibility; it does not support the cipher reading. Labelled as a consistency check, which is all it is.

**C3 — The homophone-cluster count is method-dependent.**
The "~8 families" depends on an imposed cluster count (n=25, cosine, average linkage). Only the *qualitative* finding is robust — frequent words fall into morphologically-coherent interchangeable families — and that is **equally predicted by the slot grammar**, so it does not discriminate cipher from construct. I should not have implied a specific, meaningful family count.

**C4 — Illustration "combinatoriality" is soft evidence.**
It rests on two vision-agent judgements, not measurement, and "assembled from recurring parts" is **near-trivially true of any drawing system** without a quantified baseline. The finding aligns with known scholarship (the plants are known composites) and is plausible, but it should be stated as qualitative, not as a measured structural result.

**C5 — The Naibbe match is partly by construction.**
Greshko hand-tuned the cipher's tables to reproduce VMS statistics. So "it reproduces the Voynich's properties" is an **existence proof that *some* historically-plausible cipher can**, not evidence that *the* Voynich is that cipher. The author states this honestly; I should carry the same caveat.

## D. The interpretive correction that matters most

My mid-session synthesis leaned toward "rule-governed generative system, possibly meaningless." The Naibbe cipher (Greshko 2025, *Cryptologia*) **refutes my entropy-based objection to the cipher hypothesis** — a verbose homophonic cipher reaches h₂ ≈ 2.0 while carrying real Latin/Italian — and my own finite-state grammar is fully compatible with being such a cipher's table mechanism. Combined with C1 (the line effect being possibly decorative), the honest balance shifts: **the "meaningful cipher" and "meaningless construct" hypotheses are both genuinely live, and the surface statistics do not currently separate them.** I must avoid over-correcting in either direction. What remains true and load-bearing: no key, no crib, no second text → meaning is unrecovered regardless of which hypothesis is right.

## E. Standing review checklist (apply each new result)

1. Is the number reproducible and free of a coding artifact?
2. Is the comparator fair (size, language, method)?
3. Does the result discriminate between live hypotheses, or is it equally consistent with both?
4. Am I reporting a measurement or a subjective judgement — and have I labelled which?
5. Have I stated the strongest counter-interpretation, not just my preferred one?
