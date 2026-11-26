# BUILD — news-image-20261126

## Poster layout plan (figure first)

One question this layout answers: *can a reader who missed 26 November 2026
tell, at a glance and at ~300 px wide, what the day's biggest stories were,
in what order of importance, and on what date?*

The poster is a classic front page: one masthead, one dominant lead, a
2-column-by-3-row story grid, a one-line strip, a footer. Importance falls
top to bottom, left to right.

```
+--------------------------------------------------------------+
| 1024 x 1024  |  paper #f7f2e7, ink #141414, red #a31d1d        |
|                                                              |
|  THE WORLD                      (masthead, serif, ~96 px)    |
|  THURSDAY, 26 NOVEMBER 2026  |  No. 331  |  ONE DAY'S NEWS   |
| ------------------------------------------------------------ |
|  TICKER: Nasdaq -0.62%  S&P 500 -0.25%  Dow +0.33%           |
|          KOSPI -6.16%  Nikkei -2.78%  (markets, Wed 25 Nov)  |
| ------------------------------------------------------------ |
|  LEAD (full width, ~250 px tall)                             |
|  [chart illustration: plunge then partial recovery]  | HEADLINE|
|  TARIFF SHOCK FUELS AI ROUT AS WALL STREET WHIPSAWS          |
|  3-line summary + key figures (Nasdaq fell up to 4.6%        |
|  intraday; Nasdaq 100 briefly -20% from Oct peak;            |
|  tariffs on 14 partners, max 20-40%; US markets shut Thu)    |
| ------------------------------------------------------------ |
|  GRID 2 rows x 3 cols  (~200 px per cell)                    |
|  +-----------+ +-----------+ +-----------+                    |
|  | refinery  | | asteroid  | | gauge/$   |                    |
|  | HOUTHIS   | | HERA SEES | | US ECONOMY|                    |
|  | CLAIM...  | | FLATTENED | | TOO HOT   |                    |
|  +-----------+ +-----------+ +-----------+                    |
|  | Capitol   | | football  | | globe/crack|                   |
|  | SENATOR   | | LILLE STUN| | COP31 BLAME|                   |
|  | DEMANDS.. | | BAYERN    | | GAME      |                    |
|  +-----------+ +-----------+ +-----------+                    |
| ------------------------------------------------------------ |
|  ALSO TODAY (one line, 3 items)                              |
|  Thanksgiving: US markets shut | ECB holds 2.50% | Brazil:    |
|  surplus target up to 2% of GDP by 2031                      |
| ------------------------------------------------------------ |
|  THE WORLD — Thursday 26 November 2026 — Sources: Reuters,   |
|  AP, CNN, ESA, Xinhua. Drawn in code; no photographs.        |
+--------------------------------------------------------------+
```

Layout facts (all in `draw_poster.py` as named constants):

- Canvas 1024 x 1024, 28 px outer margin, 14 px gutters between grid cells.
- Masthead band y 24–150: nameplate, date line, double rule.
- Ticker band y 156–186: five index moves, red for falls, green for rises.
- Lead band y 196–448: illustration left (300 x 220), headline + summary right.
- Grid y 476–876: 3 columns x 2 rows, each cell 313 x 198 (art 80 px,
  kicker, 2-line headline, up to 3 lines of body).
- Also-today strip y 886–946: heading + three one-liners.
- Footer y 956–996: source line, centred.

## Design choices

- **Palette (taste-skill: one system, no violet):** warm newsprint paper,
  near-black ink, one red for urgency and section kickers, one deep blue for
  charts and the asteroid panel, one green only for rising market figures.
- **Type:** DejaVu Serif Bold for masthead and headlines (newspaper voice),
  DejaVu Sans for body copy, DejaVu Sans Bold for kickers and the ticker.
  Smallest body text 13 px so the page still reads at ~300 px wide.
- **Density (motion-design three layers, applied to a still image):**
  primary = lead chart and headlines; secondary = six small coded
  illustrations, one per grid cell; ambient = rules, dots, ticker figures,
  kicker labels and the footer source line. The page is busy on purpose —
  a newspaper front page, not a minimal poster.
- **Illustrations:** every picture is drawn in code with PIL primitives
  (lines, polygons, ellipses, arcs). No photographs, no network, no fonts
  beyond the system DejaVu/Liberation set, so the run is deterministic.

## Facts used (from RESEARCH.md)

- Lead: Trump tariffs on 14 partners + AI sell-off, Wed 25 Nov trading.
  Nasdaq closed -0.62% after falling up to 4.6% intraday; Nasdaq 100
  briefly -20% from its early-October peak; S&P 500 -0.25%; Dow +0.33%
  after opening -1,100 points; KOSPI -6.16%; Nikkei -2.78%; Nvidia -3.9%.
  US markets closed Thu 26 Nov for Thanksgiving.
- G1: Houthis claim strike on Ras Tanura, Saudi Arabia's largest refinery;
  coalition says 4 drones downed over Ras Tanura, 3 more in Eastern Province.
- G2: ESA Hera images show Dimorphos flattened by a crater nearly as wide
  as the 151 m moonlet; DART struck 26 Sept 2022; Hera 25–30 km away.
- G3: US October PCE inflation 3.8% y/y (core 3.3%); Q3 GDP revised to
  4.3%; jobless claims 189,000; traders price a ~95–97% chance of a
  December Fed hike.
- G4: Senator Cory Booker demands answers from Nvidia over Jensen Huang's
  reinstatement; Huang resigned 12 Nov, reinstated Mon 24 Nov; House
  intelligence session 1 Dec, Senate banking hearing 3 Dec.
- G5: Champions League Matchday 5, Wed 25 Nov: Lille 2–1 Bayern Munich;
  Club Brugge 0–3 Liverpool; PSG 2–2 Roma; Inter 2–0 Stuttgart;
  Sporting 2–2 Man Utd.
- G6: COP31 collapsed Sun 22 Nov in Antalya; OPEC chief blames the EU,
  Pope Leo XIV laments the failure (both Wed 25 Nov).
- Strip: US markets shut for Thanksgiving; ECB deposit rate steady 2.50%;
  Brazil targets a primary surplus of up to 2% of GDP by 2031.

Deliberately NOT printed: any Brent oil price (sources conflict), the viral
infographic's UCL scores (Rotascore version used instead), any single
Selic figure for Brazil (sources conflict), a single Fed-hike probability
(shown as a ~95–97% range), and COP31's collapse is dated 22 Nov, not
presented as a 26 Nov event.

## Implementation

- `draw_poster.py` — PIL program, stdlib + Pillow only, no network, no
  randomness, no timestamps. Writes `entry.png` next to itself (or to the
  path in `sys.argv[1]`).
- `main.py` — stdlib-only entrypoint: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` (default `/output`), checks size ≤ 1 MiB and that
  the copy's sha256 matches the source.
- `entry.png` — the rendered poster, 1024 x 1024, ≤ 1 MiB.

## Verification (done locally)

- `python3 draw_poster.py` → `entry.png`, 1024 x 1024, 157,044 bytes
  (sha256 `7b55a2f4cef125b77e66e40cbd884c8260869ae5a11dbe664489f17341b78d2a`).
  Two runs of `draw_poster.py` produce byte-identical files.
- `MAKEFUN_OUTPUT_DIR=/tmp/output-test python3 main.py` run twice →
  identical sha256 both runs, matching the source file.
- Poster read back as an image and checked: date correct, headlines
  legible, no clipped or doubled text.
