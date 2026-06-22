# voynich-cryptanalysis

A reproducible, **honesty-first** computational analysis of the Voynich Manuscript (Beinecke MS 408). The goal is not to claim a decipherment — none is verified, and none is offered here — but to measure exactly what the text *is* and *is not*, reverse-engineer the script's generative grammar, and rigorously evaluate published decipherment and cipher claims against the data.

> **Honest headline:** the manuscript remains undeciphered. This project recovers the script's *form* (a finite-state word grammar), maps where the mystery actually lives, and tests the leading hypotheses — but does not recover *meaning*, because no key, crib, or second text exists to make that possible.

## What's inside

- **Full statistical characterisation** — character entropy, Zipf, word-order information, slot grammar, line-as-unit effect, Currier A/B, benchmarked against 8 languages (Latin, Italian, German, English, Finnish, Sanskrit, Arabic).
- **Reverse-engineered script grammar** — an order-3 finite-state machine over glyph-group "atoms" that generates synthetic Voynichese statistically indistinguishable from the real manuscript (94% of generated words are real Voynich words).
- **Interactive generator** (`voynich_generator.py`) — produces new Voynichese words/pages, rendered in an EVA glyph font.
- **Iconographic catalogue** — visual-morphology analysis of ~136 herbal/pharmaceutical plant folios and the diagram sections.
- **Evaluations** of recent claims: the Kondrak "Hebrew/AI" media story, Crowe (2022) "Arabic/Cathars," and Greshko (2025, *Cryptologia*) "Naibbe cipher."
- **Deliverables**: `main.{md,docx,pdf}` (report), `inventory.{md,docx,pdf}` (209-page catalogue), `herbal_catalogue.{md,docx,pdf}`, `figures/fig1–6` at 600 DPI (PDF/SVG/PNG/TIFF).

## Quickstart

```bash
# 1. transcription (LSI interlinear, included) + comparison corpora are fetched by the scripts
python3 cryptanalysis.py          # core statistics
python3 cryptanalysis3.py         # multilingual sweep + slot-cipher + finite-state tests
python3 reverse_engineer.py       # learn & validate the generative grammar
python3 figures.py                # regenerate all figures

# generate synthetic Voynichese
python3 voynich_generator.py --words 25
python3 voynich_generator.py --page --section recipe --out synthetic_page.png
```

**Prerequisites:** Python 3.10+, `numpy`, `scikit-learn`, `matplotlib`, `Pillow`. For the page renderer, place an EVA font at `assets/eva1.ttf` (e.g. the "EVA Hand 1" TTF). For PDF/DOCX builds: `pandoc` + `xelatex`.

## Data note

The source facsimile PDF, the evaluated papers, and the rendered page images are **not** committed (size / third-party copyright). The included `LSI_ivtff_0d.txt` is the public Landini–Stolfi interlinear EVA transcription. Comparison corpora are fetched at runtime.

## Key findings (one-liners)

- Conditional character entropy **h₂ ≈ 2.16** — far below any natural language; a *verbose homophonic* cipher (Greshko 2025) can reach this, a simple substitution cannot.
- Words obey a rigid **prefix–core–suffix slot grammar**; a finite-state machine reproduces ~90% of the lexicon.
- The text is written **left-to-right**, is **not boustrophedon**, and reversal/mirror reading yields nothing.
- A residual **line-as-unit** signal (~0.09 bits/word about a word's first glyph) is the one property neither the grammar nor the current Naibbe cipher reproduces — possibly scribal decoration rather than deep structure.
- No decipherment claim (Hebrew, Proto-Romance, Arabic) survives a blind-reproducibility test.

## License & status

Research code, provided as-is. Findings are exploratory and self-audited; see `main.pdf` for the full report and caveats.
