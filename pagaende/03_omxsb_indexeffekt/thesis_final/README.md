# thesis_final

Allt som behövs för att få fram uppsatsens huvudresultat: datan, koden och en fil som kör allt. Koden läser bara från `data/` och skriver bara till `results/`.

## Kör

Öppna mappen `thesis_final` i VS Code och kör `run_all.py` (Run Python File), eller i terminalen:

```
pip install pandas==3.0.5 numpy==2.5.3 scipy==1.18.1 python-docx==1.2.0 matplotlib==3.11.2
python3 run_all.py
```

Det tar cirka tio minuter. Först kontrolleras att datafilerna är exakt samma som i testet (md5 i `data/FILES.csv`). Sista raden ska vara `0 FEL`: då är huvudsiffrorna desamma som i testet 10 november 2026.

## Koden

| Fil | Vad den gör | Skriver till |
|---|---|---|
| `code/01_effect_table.py` | Effekten per period och decennium (G&S tabell I; årsraderna kommer ur data/comparison), med intervall och wild cluster bootstrap | `results/effect/` |
| `code/returns.py` | Dagliga överavkastningar mot OMXSBGI, används av 01 | |
| `code/02_fund_demand.py` | Indexfondernas köp (D), priset per köpt procent (M), vem som köper, ägarandel per år. Huvudmått sedan 11 nov 2026: C (B + V + blandfondernas OMXSB-del); B och V visas bredvid | `results/fund_demand/` |
| `code/02b_indexaffarer.py` | Indexaffärstestet (G&S regel: en fond räknas som följare om den gör minst hälften av indexaffärerna), per fond och år | `results/fund_demand/indexaffarer_fond_ar.csv` |
| `code/03_fund_demand_fi_check.py` | M med FI:s bredare D, som kontroll | `results/fi_check/` |
| `code/04_msci_overlap_match.py` | Vilka OMXSB-händelser som sammanfaller med en ändring i MSCI Sweden | `results/msci_overlap/` |
| `code/05_msci_overlap_results.py` | Effekt och M med och utan de händelserna | `results/msci_overlap/` |
| `code/06_mde.py` | Minsta påvisbara effekt för huvudtesterna | `results/mde/` |
| `code/07_controls_from_prices.py` | Kontrollvariablerna i G&S tabell 2 räknade ur kurserna för alla händelser. Ändrar ingen tabell | `results/controls/` |
| `code/09_news_screen.py` | Robusthet: effekten utan händelser med egen bolagsnyhet i fönstret | `results/news_screen/` |
| `code/10_composition_runup.py` | G&S tabell 2 (sammansättning) och tabell 4 (uppgång före beskedet), kursbanan till figur 7, M på samma händelser | `results/composition/` |
| `code/11_liquidity_and_selection.py` | G&S figur 9 (spread per år), volymens fördelning kring ändringsdagen, figur 8 (tilläggens storleksrang) | `results/liquidity/` |
| `code/12_issuance_and_omxs30.py` | G&S nyemissioner kring ändringen (aktieantalet splitjusterat sedan 11 nov 2026) och tabell 8 (OMXS30) | `results/other_tests/` |
| `code/13_extreme_values.py` | Robusthet för extremvärden: tabell 2:s rader winsoriserade 1/99, utan \|CAR\| > 20 och utan Sivers, median, och M utan de 12 nyhetshändelserna | `results/extreme_values/` |
| `code/14_near_additions_control.py` | Tillägg och borttag mot nästan tillagda och nästan borttagna (T5v ur runda 2) | `results/near_additions/` |
| `code/15_reversal.py` | Återgången efter ändringen, CAR [ED, ED+10] och [ED, ED+20], och uppgången [AD, ED−1] (ur del1.py) | `results/reversal/` |
| `code/16_twins.py` | Tvillingar: indexslaget mot systerslaget i samma bolag, placeboinferens och A/B-revisionen (ur twin_*.py och ab_revision.py) | `results/twins/` |
| `code/panel.py`, `code/panel_runda3.py` | Läser hela kurspanelen, används av 07, 11 och 12 | |
| `code/output/01_…` till `26_…` | En fil per tabell eller figur, i Greenwood och Sammons ordning (figur 1, tabell 1–2, figur 2–3, tabell 3, figur 4–5, tabell 4, figur 6, tabell 5–6, figur 7–8, tabell 7–13, bilaga A2–A6). Varje fil läser bara från `results/`, kontrollerar sina siffror mot källfilen och skriver en egen `.docx` (figurer även `.png`). Noterna till filerna 06, 08–10, 13, 14, 16, 17, 19–21, 24 och 25 är utkast (`# utkast`) | `results/tables/` |
| `code/output/_style.py` | Gemensam Word- och figurstil, numreringen av tabeller och figurer (`NUM`) och metodtexterna i noterna | |
| `code/output/99_all_tables.py` | Alla tabeller och figurer i ett dokument, `all_tables.docx` | `results/tables/` |
| `code/08_check_numbers.py` | Jämför huvudsiffrorna, och siffrorna i steg 07 och 09–16, med väntade värden | `results/check.txt` |

## Datan

| Fil | Källa | Innehåll |
|---|---|---|
| `data/events/omxsb_changes_nasdaq_2007_2026.csv` | Nasdaq, RIC från LSEG | Alla 536 tillägg och borttag: bolag, ISIN, RIC, beskedsdag, ändringsdag, länk till Nasdaqs besked |
| `data/events/omxsb_changes_corrected_2007_2026.csv` | Härledd | Händelserna efter rättelserna 3 nov, med flagga för aktiesplit. Används för D och M |
| `data/events/omxsb_changes_with_car_2007_2026.csv` | Härledd | Händelserna med beräknad överavkastning (CAR) |
| `data/prices/stock_prices_daily_2004_2026.csv.gz` | LSEG | Daglig kurs, totalavkastning, volym, börsvärde, aktieantal, köp- och säljkurs för 186 aktier |
| `data/prices/index_levels_daily_2004_2026.csv` | LSEG | OMXSPI, OMXSGI, OMXS30, OMXS30GI, OMXSBGI och OMXSBCAPGI per dag |
| `data/prices/all_stocks_daily_2004_2012.csv.gz`, `…2013_2019…`, `…2020_2026…` | LSEG | Hela kurspanelen: alla 1 526 aktier med RIC .ST, samma kolumner som ovan. Tre filer för att varje ska vara under 50 MB. Samma data som `data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet` |
| `data/prices/nordea_tieto_daily_lseg.csv` | LSEG | Nordea och Tieto, som saknas i panelen |
| `data/index/omxsb_constituents_2009_06_01.csv` | Nasdaq | Bolagen i OMXSB 1 juni 2009, utgångspunkt för medlemskapet i steg 11 |
| `data/index/omxsb_members_by_review_verified.csv` | Härledd | Medlemmarna i OMXSB efter varje översyn, verifierade 1 nov |
| `data/controls/` | LSEG | Marknadsplats per aktie och antal vinstprognoser per månad, till kontrollerna i steg 07 |
| `data/events/additions_and_near_additions_2007_2026.csv` | Härledd | Tillägg och nästan tillagda aktier, urvalet i nyemissionstestet och i steg 14 |
| `data/events/omxsb_deletion_flags_2007_2026.csv` | Härledd | Borttagen med flaggor för bud, fusion, avnotering och ändrat aktieantal. Styr urvalet |
| `data/events/news_screen_extreme_events.csv` | Egen genomgång | De 24 händelserna med störst CAR: hade bolaget en egen nyhet i fönstret? Med källa |
| `data/funds/index_fund_list_with_mandates.csv` | Fondernas egna dokument | Vilka fonder som följer OMXSB (grupp B, V, C eller X), från och till vilket datum, med källa |
| `data/funds/index_fund_list_sources.md` | Fondernas egna dokument | Källorna till fondlistan, fond för fond |
| `data/funds/fund_holdings_lipper_around_events_2007_2026.csv.gz` | LSEG/Lipper | Varje fonds innehav i aktien före beskedet och efter ändringen |
| `data/funds/fund_holdings_request_list.csv` | Härledd | Händelser och datum som hämtningen från LSEG byggde på |
| `data/funds/fund_aum_shof_monthly.zip` | SHoF | Fondernas förmögenhet per månad |
| `data/funds/fund_ids_shof.csv` | SHoF | Fondernas id, ISIN och startdatum |
| `data/funds/fund_list_fi_quarterly_2018_2026.csv` | FI | Alla svenska fonder per kvartal: förmögenhet, aktiv risk, jämförelseindex |
| `data/funds/fund_net_buying_fi_by_event_2019_2026.csv` | Härledd ur FI | Indexfondernas nettoköp per händelse, kontroll av D |
| `data/msci/msci_sweden_changes_2007_2026.csv` | MSCI via LSEG | Ändringar i MSCI Sweden med besked- och ändringsdag |
| `data/comparison/previous_run_demand_and_ownership_by_year.csv` | Härledd | Köp och ägarandel per år från en tidigare körning, för jämförelse |
| `data/comparison/replication_effect_by_year.csv` | Härledd | Effekten år för år från replikeringen (tabellen räknas nu i steg 01) |
| `data/comparison/previous_run_*.csv` | Härledd | Resultaten från körningarna 30 okt till 2 nov och kontrollsiffrorna 11 nov. Steg 11 till 16 jämför sig med dem |
| `data/twins/` | Härledd | Tvillingparen, den mekaniska rensningen och de bortrensade händelserna (steg 16) |
| `data/prices/tvilling_priser_lseg.csv`, `…_2.csv` | LSEG | Kurser för NCC A, Sweco A, Bonava A och Ratos A, som saknas i panelen (steg 16) |

`data/FILES.csv` har samma lista med antal rader, storlek, md5 och var filen låg tidigare i repot.

## Det som inte är med här

Kontrollgrupperna, återgången efter ändringen, tvillingaktierna och förutsägbarheten körs fortfarande från sina gamla skript i repot (`theses/03_omxsb_indexeffekt/historik/claude_checks/`, som hette `code/claude_checks/` före 13 nov 2026). Hela kurspanelen finns nu här, så de kan flyttas hit.

Av Greenwood och Sammons test går två inte att göra i Sverige: migrationer mellan index (tabell 3, figur 4 till 6) och implementation shortfall. Steg 07 har ingen egen Word-tabell; det ändrar ingen tabell.

## Deklarationer

`declarations/` har en fil per beslut, skriven med tidsstämpel innan något kördes: nyhetsgenomgången, urvalsregeln för borttag, steg 10 och flytten av steg 07, 11 och 12.

## Licens

Kurser, index och fondinnehav från LSEG och MSCI är licensierade via SSE. De får användas i uppsatsarbetet men inte spridas vidare. Repot ska därför vara privat.
