# Reverse-engineering the rosettes foldout (f85–86)

Last updated: 2026-06-22

The rosettes page is the largest and most structurally complex illustration in MS 408 — a six-panel foldout. Folios in the transcription: `f85r2, f86v3, f86v4, f86v5, f86v6`. This note separates **layout** (what the picture is) from **text** (the writing on it), and flags clearly what is visible in the available low-resolution facsimile vs. what is established from high-resolution scans / scholarship.

## Layout (picture-level)

**Visible in this facsimile (native image ~1536 px for the whole 6-panel sheet — low for this page):**
- A **3×3 arrangement of nine circular "rosettes"** with a prominent **central rosette** acting as a hub.
- Rosettes are individually elaborate: radiating blue petals, concentric patterned rims, radial spokes, small repeated rim elements; the **bottom-left rosette shows dense structures around its rim** (consistent with the documented "city/buildings" rosette).
- Faint connecting bands between circles.

**Documented in scholarship / high-res scans (NOT resolvable at this scan resolution — cited, not verified here):**
- The nine rosettes are linked by **"causeways"** (banded paths), several with small structures at their ends.
- One rosette contains a **"castle"/walled city with swallowtail ("Ghibelline") merlons and towers**. The swallowtail merlon is a Northern-Italian Ghibelline architectural feature — an art-historical marker consistent with the **1404–1438** radiocarbon date and a Northern-Italian origin.
- **Sun and moon** motifs and **T-O-map-like** elements appear among the rosettes.
- The whole sheet is widely interpreted as a **map** (geographic and/or cosmological) — the only Voynich page with genuinely map-like global structure. This remains an *interpretation*, not a proven reading.

**Reverse-engineered structure:** each rosette instantiates the same disk-primitive grammar found elsewhere (rim + concentric rings + radial spokes + central medallion), and the foldout = **(disk grammar × 9) + a connector/causeway operator + corner features (castle, sun, moon)**. It is the manuscript's combinatorial visual vocabulary scaled up to a full composition.

## Text (script-level) — the rigorous part

Extracted from the transcription: **1,472 tokens** (1,287 radial-paragraph `P` + 185 circular-centre `Cc`), all in **Currier language B**.

| Property | Rosettes text | Body text | Reading |
|---|---|---|---|
| Hapax rate | **71%** | 70% | **Ordinary** — not a name/legend layer |
| Top words | aiin, or, ar, ol, dar, daiin, qokar… | daiin, ol, chedy, shedy… | ordinary Currier-B prose |
| Onset | o 17, qo 15, a 11, ch 11 | ch 19, qo 18, d 11 | mildly shifted, within normal range |
| `p/t`-initial | 5% | 4% | slight paragraph-start gallows |

The six circular centre texts (`@Cc`, candidate per-rosette "titles") share the label register's `o-/ot-` onset but are ordinary in length and statistics — not short distinctive titles.

**Key finding:** unlike the zodiac/pharma *labels* (85–97% hapax, name-like, distinct register), the rosettes text is **statistically ordinary running Currier-B prose** (71% hapax, normal vocabulary). There is **no detectable map-legend or place-name signature** — the writing around the circles reads like the rest of the manuscript's paragraphs.

## Crib verdict

The rosettes foldout is the strongest *picture-level* case in the manuscript: its global structure genuinely looks like a map/cosmological diagram, and the (cited) Ghibelline-merlon castle is a real dating/localizing anchor pointing to early-15th-century Northern Italy. But the **text yields no crib** — it is ordinary Voynichese with no legend-like or directional vocabulary, so it will neither confirm the map reading nor label the places. As everywhere in this project: the **iconography advances** (we can say what the page probably *is*), the **script does not** (we cannot read what it *says*).

*Audit note:* the castle/merlon and causeway features are **cited from scholarship**, not verified from this low-resolution facsimile; the text statistics are measured and reproducible.
