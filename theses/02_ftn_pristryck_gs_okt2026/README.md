# 02 Pristryck när Fondtorgsnämnden flyttar premiepensionen (oktober 2026)

**Status:** VILANDE sedan 29 oktober 2026. **Ingen avkastning kring ett FTN-datum har räknats.** Spärren `UNBLIND = False` sitter kvar i `kod/ftn_eventstudy.py` och `kod/dilution.py`. OMXSB-replikationen, som var del 1 här, blev en egen uppsats: alternativ 03. Den nuvarande uppsatsen (`../03_omxsb_indexeffekt/thesis_final/`) innehåller ingen FTN-del.
**Senast ändrad:** 29–30 okt 2026 (plan och design). Mappen samlades här 13 nov 2026.

## Frågan

"Pre-announced, uninformed, and large: the price of moving the premium pension". När FTN väljer bort en fond säljer Pensionsmyndigheten en stor del av fonden på en i förväg känd dag, och 94 procent av pengarna flyttas för att sparare inte svarade på ett brev. Det är en daterad efterfrågechock utan information. Frågan är hur mycket den rör aktiekurserna och vem som betalar.

- **Ankare:** Greenwood & Sammon (2025, JF), "The Disappearing Index Effect".
- **Metod (plan 25 okt):** del 1 replikation av G&S på OMXSB, del 2 FTN-pristryck (eventstudie med dos, ekvation 5–6), del 3 vem som betalade (utspädning och swing pricing).
- **Ändring 29 okt:** del 1 utvidgades till G&S fem förklaringar på OMXSB 2007–2026. FTN behölls bara som en ny miljö där samma test körs; beskedet kommer månader före försäljningen och skiljer förutsägbarhet från händelselikviditet. Struket: vem som betalade, kostnaden i kronor, swing pricing och kvadratrotslagen. `plan/STATUS.md` beskriver ändringen. `design/01_DESIGN.md` och `design/thesis2_method.tex` beskriver fortfarande den äldre tredelade strukturen.

## Innehåll

| Mapp | Vad | Datum |
|---|---|---|
| `plan/PLAN.md` | Planen i ett dokument: kursregler, frågan, delar och hypoteser, data, arbetsfördelning | 25 okt (banner 1 nov) |
| `plan/STEPS.md` | Sju grindar och veckosteg med ägare | 25 okt |
| `plan/STATUS.md` | Läget 29 okt, med tillagda banners 1–4 nov om OMXSB-arbetet (se alternativ 03) | 29 okt – 4 nov |
| `design/00_VALIDATION.md` | Deep research: håller designen? | 11–12 okt |
| `design/01_DESIGN.md` | Förhandsplanen: mått, skattning, inferens, styrka | 12 okt, ändrad 30 okt |
| `design/03_DATA.md` | Vad som finns, vad som saknas, avsnitt E = datum för handledarens godkännande | 12 okt (sökvägar 25 okt) |
| `design/THESIS_IN_PLAIN_WORDS.md`, `.docx` | Uppsatsen i klartext, version 2.4, del A–H | 25 okt |
| `design/thesis2_method.tex`, `.pdf` | Metodnoten med ekvationer och ärlig bedömning | 14 okt |
| `outline/thesis2_outline.md` | Avsnitt för avsnitt, sidbudget | 25 okt |
| `research_2026-10-11/` | Djupgenomgången som valde designen: frågekarta, vinnarmönster, ankarsökningar, nya fakta, förslaget, blind referent. `agentrapporter_raa/` innehåller två råa agentrapporter | 11 okt |
| `text/` | LaTeX-skelett, ett tomt avsnitt per kapitel | 27 okt |
| `kod/` | Analyskoden, se nedan | 25–27 okt |
| `sammanfattningar_2026-10/` | Äldre sammanfattningar (Word/PDF), ersatta av klartextversionen | okt |
| `tabellanteckningar/NOTES.md` | En mening per tabell (aldrig ifylld) | 27 okt |

Litteraturlistan för den här designen (`literature_verified.md`, `references.bib`) underhålls i `../03_omxsb_indexeffekt/litteratur/`.

## Koden (`kod/`)

Sökvägarna rättades 13 nov 2026: skripten hittar repots `data/` och skriver till `output/` i den här mappen.

| Fil | Gör | Körs nu? |
|---|---|---|
| `eventstudy.py` | Motorn: faktormodell, CAR, BMP och Kolari–Pynnönen, klusterrobust OLS, wild cluster bootstrap, randomiseringsinferens | Ja. `python3 kod/eventstudy.py` kör ett självtest (godkänt 13 nov) |
| `power.py` | Minsta påvisbara effekt per tabell | Ja (kontrollerat 13 nov) |
| `parse_fi.py` | FI:s innehavszippar till långa csv-filer | Ja, tar sökvägar som argument |
| `pressure.py` | Dos per aktie och tranchdag (ekvation 5–6), inga avkastningar | Nej: kräver kvartalsfilerna `fi_holdings_<q>.csv` från `parse_fi.py` |
| `ftn_eventstudy.py` | Tabell 3–4, figur 3 | **Spärrad** (`UNBLIND = False`). Kräver dessutom `data/input/round_dates.csv` och `factors_daily.csv`, som inte finns |
| `dilution.py` | Tabell 5, utspädning för kvarvarande sparare | **Spärrad**, samma spärr |
| `replication_omxsb.py` | Skriptversionen av OMXSB-tabell 2 (2013–2026) | Nej: kräver `factors_daily.csv`, som inte finns (`data/input/omxsb/tracker_aum.csv` finns). Notebooken i alternativ 03 gjorde jobbet |

## Data

Allt ligger i den gemensamma `data/` (`data/README.md` visar vad som används av vilket alternativ):
- Rådata: `data/raw/ppm/`, `data/raw/ftn/`, `data/raw/fi/`, `data/raw/shof/` (Valuations och Reinvestments delas för hand, inte i git), `data/raw/lseg/panel_2012_2026/`, `panel_eu/`, `panel_2005_2026/fund_nav_tna_daily.csv`.
- Handbyggt: `data/input/swing/`, `data/input/holdings_external/`, `data/input/lseg/`.
- Härlett: `data/derived/ppm/`, `ftn/`, `exit_days/`, `measurements/`, `facts/`, `shof_monthly/`.
- Byggkod: `data/build/detect_exit_days.py`, `build_ppm_panel_2018.py`, `build_ppm_panel_2022.py`, `swing_build_outputs.py`, `shof_monthly.py`, `agent_runs/`.

## Om alternativet tas upp igen

1. Klug godkänner specifikationerna. Datumet skrivs i `design/03_DATA.md` avsnitt E, och `UNBLIND = True` sätts i samma commit.
2. `design/01_DESIGN.md` skrivs om till strukturen från 29 okt (`plan/STATUS.md`, punkt 7).
3. Tranchdagarna för småbolagsrundan dateras efter SHoF:s uppdatering. Kör `data/build/detect_exit_days.py` igen.
4. Bevakning från 29 okt: FI:s innehav för 2026Q3, Indecaps överklagande av den globala aktiva rundan och Riksrevisionens granskning av fondtorget.
