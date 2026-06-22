# Project status

Last updated: 2026-06-22

One-line state: **the script is statistically characterised and its generative grammar reverse-engineered; the imagery is read at the picture level; the meaning of the text is not recovered and likely cannot be from internal evidence alone.**

## Done

- **Page inventory** — all 209 facsimile images catalogued (`inventory.*`).
- **Statistical characterisation** — entropy (h₂ ≈ 2.16), Zipf, word-order information, slot grammar, Currier A/B, benchmarked against 8 languages incl. Arabic/Sanskrit (`cryptanalysis*.py`, `figures/fig1–5`).
- **Hypothesis tests** — simple/verbose/position-dependent substitution, reversal/mirror, boustrophedon, non-European languages — all excluded with reproducible evidence (`decipher_framework.py`).
- **Reverse-engineered script grammar** — order-3 finite-state machine reproduces the manuscript (94% precision / 90% recall); interactive generator with EVA rendering (`reverse_engineer.py`, `voynich_generator.py`, `fig6`).
- **Iconographic reverse-engineering + crib hunts** — herbal (`herbal_catalogue.*`), zodiac, rosettes foldout, astronomical volvelles, balneological plumbing, cross-section labels (`docs/*`). Result: imagery legible, script not.
- **Claim evaluations** — Hebrew/AI media story, Crowe (2022) Arabic/Cathars, Greshko (2025) Naibbe cipher.
- **Self-audit** — adversarial review with corrections recorded (`docs/AUDIT_LOG.md`).
- **Report** — `main.{md,docx,pdf}` (10 pp), repo on `infigenie/voynich-cryptanalysis`, tags `v0.1`, `v0.2`.

## Settled conclusions (high confidence)

- Genuine early-15th-century Northern-Italian artefact (radiocarbon 1404–1438; Ghibelline-merlon architecture).
- ~23-glyph alphabet-scale script, written left-to-right, two Currier "dialects" = one engine at two settings.
- Word-forms are finite-state/templatic to a degree no natural language matches.
- Not gibberish, not a simple cipher, not any tested natural language by simple substitution.

## Open (genuinely undecided)

- **Cipher vs. construct.** A verbose homophonic cipher (Naibbe-class) of real Latin/Italian is viable and reproduces most statistics; an elaborate meaningless construct is equally consistent. Internal statistics do not separate them.
- **Does a plaintext exist at all?** Unresolved.

## Blocked (and why)

- **Reading the text.** Blocked on the absence of (a) a key, (b) a crib/bilingual, or (c) a second document in the script. No internal analysis can substitute for these. The zodiac month-names (later Latin hand) are the only near-crib and do not align to the Voynichese labels.

## What would change the verdict

1. A **second text** in the same script surfacing anywhere.
2. A genuine **bilingual** or a verified **crib** (a known name/word at a known location).
3. A **recovered cipher key / table set** (e.g. a historical document describing the system).
4. A decipherment that passes the **blind-reproducibility test** — fixed rules, applied to an unseen page, yielding coherent on-topic language. None has.
