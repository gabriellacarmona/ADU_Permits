# ADU Permits in the City of Los Angeles, 2017–Present

Analysis of Accessory Dwelling Unit (ADU) permitting in the City of Los Angeles built
from LADBS building-permit records: a documented construction pipeline (what counts as a
valid ADU permit, completed vs. in-progress), validation against published academic and
agency counts, and maps/animations of ADU growth citywide and in three focus Community
Plan Areas — **Arleta–Pacoima**, **Northeast Los Angeles**, and
**West Adams–Baldwin Hills–Leimert**.

**Read the report:** <https://gabriellacarmona.github.io/adu_permits/> *(passphrase required — ask Gabriella)*

Gabriella Carmona · UCLA Latino Policy & Politics Institute

## What's here

| Path | What it is |
|---|---|
| `adu_permit_pipeline.Rmd` | The full analysis: step-by-step filtering log, yearly/CPA tables, CPA rankings, validation, histograms, parcel-level maps, and GIF generation |
| `docs/index.html` | The knitted report, **encrypted** (StatiCrypt) and served by GitHub Pages at the link above; all figures and animations are embedded inside it |
| `data/adu_projects.csv` | One row per ADU project (permit + its supplements), 2017–present |
| `data/adu_properties_by_pin.csv` | One row per property (PIN): permits filed, units completed / in progress |
| `data/sf_parcels_by_cpa.csv` | Single-family parcel counts per CPA (County Assessor 2025 roll) — ranking denominator |
| `data/cpa_boundaries.geojson` | Community Plan Area boundaries (LA City Planning GeoHub) |
| `data/parcels_focus.geojson` | Parcel polygons for the three focus CPAs (County Assessor) |
| `scripts/fetch_parcels.py` | Rebuilds `parcels_focus.geojson` from the Assessor's feature service |
| `publish.sh` | One-command re-knit + encrypt + push (see below) |

## Raw data (not in the repo)

The two LADBS extracts are ~300 MB each, over GitHub's file limit. Download them from
the LA Open Data portal and place them next to the `.Rmd`:

- [Building Permits Issued Between 2010 and 2019](https://data.lacity.org/City-Infrastructure-Service-Requests/Building-and-Safety-Building-Permits-Issued-Betwee/)
- [Building Permits Issued from 2020 to Present](https://data.lacity.org/City-Infrastructure-Service-Requests/Building-and-Safety-Building-Permits-Issued-from-2/)

The `.Rmd`'s YAML params name the expected files; update the two paths (or the filenames)
if your download is a newer refresh, and re-check the Step 3 typo list against any
project exceeding ~10 units.

## Reproducing / updating

Requires R with: `dplyr`, `tidyr`, `readr`, `stringr`, `purrr`, `tibble`, `ggplot2`,
`lubridate`, `scales`, `sf`, `knitr`, `kableExtra`, `rmarkdown`, `png`, `gifski` —
plus Node with [StatiCrypt](https://github.com/robinmoisson/staticrypt)
(`npm install -g staticrypt`) for the report encryption, and a `.report_password`
file in the repo root (one line: the passphrase; it is gitignored and never committed).

To update the published report after editing the `.Rmd` (or refreshing the data):

```bash
./publish.sh "describe your change"
```

That re-knits the report (GIFs included), encrypts it with the passphrase from
`.report_password`, writes it to `docs/index.html`, and pushes; GitHub Pages picks it
up within a couple of minutes. Only the encrypted page is ever committed — the plain
HTML, the PDF, and the standalone figure files stay local so the passphrase actually
protects the content.

## Method in one paragraph

ADU permits are identified by the LADBS structural-inventory fields `ADU_CHANGED` +
`JUNIOR_ADU` (net unit changes, populated from 2017). Supplemental permits are collapsed
into their parent permit ("project"); units are netted so corrections cancel; four
square-footage-as-unit-count typos are fixed; projects netting ≤ 0 units (demolitions,
removals) and invalid permits (expired/closed/refunded/revoked with no CofO anywhere in
the permit chain) are dropped. Completed = CofO date or CofO-issued/corrected/finaled
status; everything else still alive is in progress. CPA names are normalized to the
GeoHub boundary spellings (Central City + Central City North → Downtown). Full details,
counts dropped at each step, and validation against Crane (2020), Brueckner & Thomaz
(2024), HCD APRs, and Crosstown LA are in the report.
