# Crib hunt — the zodiac labels

Last updated: 2026-06-22

The zodiac section (12 surviving folios; Capricorn & Aquarius folios are lost) shows circular diagrams with ~30 "nymph" figures per sign, each tagged with a short Voynichese label and a star. Labels are the best crib candidate in the manuscript: if anything is a *name list*, it is these. Below, the labels are extracted from the Takahashi/EVA transcription (locus type `L` on `$I=Z` pages), one label per nymph in ring order. 296 labels total.

## Findings

| Test | Result | What it means |
|---|---|---|
| **A. Uniqueness** | 296 labels, 251 distinct, **88% hapax** | More unique than body text (71% hapax) — modestly name-like, but small-sample, so weak. |
| **B. Morphological register** | labels onset **ot- 27%, ok- 27%, o- 25%, qo- ~0**; body onset **ch- 20%, qo- 19%** | **Strong, robust.** Zodiac labels are a *distinct register* from running text — `ot/ok/o`-heavy and `qo`-poor. They share a common frame. |
| **C. Cross-sign label-pool overlap** | mean Jaccard **0.014**; only 2 labels recur on ≥4 signs | **Decisive — rules out a hypothesis.** Signs do **not** reuse a shared pool of ~30 day/degree labels. The labels are *not* a repeated ordinal counter. |
| **D. Sequential drift around rings** | adjacent-label edit distance 4.33 ≈ random-in-ring 4.40 | No smooth "counter" progression around the ring (not decisive against spelled-out numbers, but no obvious ordinal pattern). |
| **E. Affix-stripped cores** | 216 distinct cores from 296 labels after stripping `o/ot/ok/ote/oke-` | Structure is **[shared onset] + [unique core] + [common suffix -y/-al/-dy]**; cores remain highly diverse. |

## Interpretation (with the standing audit checklist applied)

- **B and C are real, load-bearing results.** The labels form a morphologically distinct class (B), and that class is *not* a shared ordinal system reused across signs (C). C genuinely discriminates: it kills the "each sign carries the same 30 day/degree labels" reading.
- The labels behave like **~296 distinct designations sharing a common naming frame** — exactly the surface a *name list* would have (e.g., decan/star names, each unique, all carrying a common particle).
- **One intriguing-but-inconclusive thread:** ~79% of labels begin with `o/ot/ok`. A shared onset on a list of names is what a **definite-article prefix** looks like (Arabic `al-` prefixes most catalogued star names; Romance `il-/el-`). This is suggestive — but it is *exactly* the path Crowe (2022) followed to "Arabic," which then failed blind reproducibility, and the onset varies (`o` vs `ot` vs `ok`) rather than being one fixed morpheme.

## Why the crib does not close

1. **No catalog anchor.** Even granting the labels are names, there is no bilingual or known star/decan catalog they demonstrably map onto. Past attempts to align them to Arabic star names (Crowe) do not reproduce.
2. **Procedural generation explains the same statistics.** The reverse-engineered grammar already produces unique words sharing an onset class; "unique, name-like, common-frame labels" is equally what a constructed system yields. The labels' statistics do not, by themselves, prove they encode names.
3. **The known anchor isn't machine-readable here.** The calendar crib that *does* exist — month names (`Mars`, `May`, …) written beside some wheels — is in a **later Latin hand**, not in the Voynichese label stream, and the Voynichese labels show no recoverable alignment to it from these statistics.

## Honest verdict

The crib hunt **sharpens the target without unlocking it.** It establishes that the zodiac labels are a genuinely distinct, name-like register (the right place to look), and it rules out the shared-ordinal-counter reading. But it yields **no readable plaintext**: no catalog anchor, an onset pattern that is suggestive but matches no language cleanly, and statistics a constructed system reproduces. Net: a constraint on future attempts, not a decipherment.

## Calendrical framing of the zodiac (added 2026-06-22)

The surviving zodiac runs **Pisces → Sagittarius** (doubled light/dark folios for several signs); **Capricorn and Aquarius are missing**. Iconographic ("picture-level") reading:

- The wheels are a **spring-starting calendar**: 12 signs ≈ 12 months, ~30 nymphs/sign ≈ ~30 days, ≈ 360 total. A Pisces/Aries (≈ March) start is the *normal* medieval European convention (March-25 Annunciation / "Lady Day" New Year, used widely in Europe; England until 1752) — itself the descendant of the old Roman March New Year.
- **Why Capricorn & Aquarius are absent:** most parsimoniously, the *opening leaf of the zodiac quire is physically lost* (the MS is missing ~14 folios). In a spring-starting cycle those two winter signs precede Pisces and sit on the lost first folio — so their absence follows from the spring start + a missing leaf, not necessarily a deliberate calendrical omission. (They do coincide with the old Roman winter "dead period" later filled by Jan/Feb — an apt resonance, but not needed to explain the gap.)

Historical note (corrected): January 1 became the Roman **consular/civil New Year in 153 BCE** (Livy; consuls moved to Jan 1 over the Celtiberian revolt), *before* Caesar. Caesar's 45 BCE reform was the *solar* Julian calendar, retaining Jan 1; the "Caesar chose Jan 1 to honor Janus" story is a popular misconception.

**Crib limit:** the calendar frame is real and decodes the diagrams' *purpose*, but the ~30 labels/sign do **not** behave as a shared day-counter (cross-sign Jaccard ≈ 0; no sequential ring drift), so the labels do not decode as day numbers. Picture-level reading advances; text-level reading does not.
