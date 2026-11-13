# Historik: OMXSB-arbetet före thesis_final (25 oktober – 10 november 2026)

**Inget här gäller.** Det som gäller är `../thesis_final/`. Paketen ligger kvar med sina ursprungliga namn så att gamla hänvisningar går att följa. Gamla sökvägar slås upp i `arkiv/repo_historik/FLYTTKARTA_2026-11-13.tsv`. Skripten är sparade exakt som de kördes och pekar därför på den gamla strukturen (`output/…`, `code/…`). De ska läsas, inte köras om.

Där koden låg separat i `code/build/` eller `code/notebooks/` har den lagts i en undermapp `kod/` i det paket den skrev till.

Status:
- **Källa till thesis_final**: filer härifrån är indata eller förlaga till `thesis_final` (se `thesis_final/data/FILES.csv`).
- **Ersatt**: en senare version gör samma sak.
- **Utforskande**: prövat, ingår inte i uppsatsen.
- **Källprov**: datatillgång prövad, inga ekonomiska resultat.
- **Beslutsunderlag**: läsning och bedömning, inga nya skattningar.

| Datum | Mapp | Vad | Utfall eller beslut | Status | Läs först |
|---|---|---|---|---|---|
| 25 okt | `omxsb_replication/` (+ `kod/replication_omxsb.ipynb`) | Första replikationen av G&S på OMXSB 2013–2026 | CAR för 380 händelser, indexfondernas nettohandel ur FI, 36 tabeller och 6 figurer | Ersatt av 2007-körningen | `exhibits_manifest.md` |
| 29–31 okt | `omxsb_replication_2007/` (+ `kod/`: notebook, `mechanisms_2007.py`, `period_sensitivity.py`, `trend_tests.py`, `regime_2023.py`, `deletions_clean_table.py`) | Replikationen 2007–2026 (536 händelser, 39 översyner), G&S fem förklaringar, periodlängd, trendtester, annonseringsregimen 2023 | Tabell 2 med fyra lika femårsperioder; flaggade strykningar | **Källa till thesis_final** (`events_car.csv`, strykningsflaggor, mekanismernas jämförelsesiffror) | `CHECK.md`, `mechanisms/RESULTS.md` |
| 29–30 okt | `slides_seminarium_20261029/` (+ `kod/slides_tables.py`) | Seminariedecket (`main.tex`; `main_results.tex` är detaljversionen) | – | Historik | `main.tex` |
| 31 okt | `omxsb_audit_20261031/` (+ `kod/`) | Granskning av replikationens indata och resultat: baslinje mot rättad körning, dataluckor | Rättelser och datalucklista | Historik (granskning); följdes av rättelserna 1 och 3 nov | `DATALUCKOR.md` |
| 31 okt | `omxsb_extension_20261031/` (+ `kod/`) | AP3/AP4 mot FI-fonder kring indexändringar, migrationsscreen, kandidatpilot, rättade etiketter | AP-fondernas innehav: intervallen innehåller noll | Utforskande | `UTFORT_OCH_RESULTAT.txt` |
| 1 nov | `omxsb_robusthet_20261101/` (+ `kod/`, `design/`, `robusthet_repair_20261101/`, `rot_20261101/`) | Rättad kontrollanalys version 5: T2 panelmatchning, T5 nästan tillagda. Här ligger också arbetsstrukturen, tolkningsreglerna och rättelsespecifikationen från 1 nov | T2 skattad; T5 spärrad av olösta medlemsuppgifter; tidigare påståenden tillbakadragna | Ersatt (nästan tillagda: `thesis_final` steg 14) | `RESULTAT.md`, `design/OMXSB_struktur.md` |
| 1–5 nov | `claude_checks/` | Claude-rundorna 2–12, var och en deklarerad före körning (`rundaN_deklaration.md`), plus MSCI-tvillingar, ägarkontroll, rättelserna 3 nov, tabell 1, fondklassningen 4 nov och splitfaktorn 5 nov. `lokal_korning_rot_20261101/` är den lokala körningen 1 nov som låg i repots rot | Se `RESULTAT_2026-11-01.md`, `RESULTAT_2026-11-02.md` och `RATTELSER_2026-11-03.md`; rättelserna gäller före de två resultatfilerna | **Källa till thesis_final** (större delen av `thesis_final/data/` och förlagan till steg 07 och 10–16) | `README_analyser.md`, `RATTELSER_2026-11-03.md`, `GS_AVSTAMNING.md` |
| 1–2 nov | `omxsb_open_questions_20261102/` | Daterade kontrollgrupper ur Nasdaqs historiska listor, prisbana, varaktighet, retention | Tillägg +1,60 pp och borttag −1,33 pp mot daterade kontroller; den kausala förklaringen inte identifierad | Utforskande | `RESULTAT.txt` |
| 2 nov | `omxsb_followup_20261102/` (+ `kod/`) | Ägare, mandat och volym, med omkörningsbara moduler | – | Utforskande | `START_HERE.txt`, `RESULTATKORT.txt` |
| 2 nov | `omxsb_broadening_20261102/` (+ `kod/`) | Avgränsad breddning: fondbytare, prismodeller, blankning, designgräns | – | Utforskande | `RESULTAT.txt` |
| 2 nov | `omxsb_execution_followup_20261102/` (+ `kod/`) | Handel efter offentligt besked, samma fonders köp över tid, spararkostnad | Tillägg +2,31 pp mot OMXSBGI 2017–2025; mindre och osäkert mot kontrollaktier | Utforskande | `REPORT.txt` |
| 2 nov | `omxsb_mechanism_frontier_20261102/` | Antal fondägare efter tillägg, per jämförelseindex | +9,94 ägare, varav +8,54 i fonder med OMXSB i jämförelseindexet | Utforskande | `RESULTAT.txt` |
| 2 nov | `omxsb_attention_dd_20261102/` | Kan ett mått på uppmärksamhet tillföra något? | Ja till att pröva, villkorat på data; inte genomfört | Beslutsunderlag | `DD.txt` |
| 2 nov | `omxsb_winner_architectures_20261102/` | Genomgång av alla 25 finansvinnare: vilka typer av bidrag | Mekanismidentifiering är inte det enda giltiga bidraget | Beslutsunderlag | `SAMMANFATTNING.txt` |
| 2 nov | `omxsb_overview_20261102/` | Samlad genomgång av allt fram till 2 nov, med filkarta | Resultat finns, men ingen identifierad förklaring till priset | Beslutsunderlag | `LAS_FORST.txt` |
| 3 nov | `omxsb_contribution_round_20261103/` | Vilka fondpositioner bär kapitalförändringen vid tillägg | Nya ägarpositioner +0,954 pp av börsvärdet | Utforskande | `RESULTAT_OCH_BESLUT.txt` |
| 3 nov | `omxsb_design_frontier_20261103/` | Bästa återstående fråga: ägarbasens exponering mot fonduttag (Greenwood & Thesmar 2011) | Data räcker inte; inte genomfört | Beslutsunderlag | `BESLUT_SV.txt` |
| 3 nov | `omxsb_shof_pilot_20261103/` | SHoF/Morningstar-hämtning efter inloggning | Hämtningen genomförd för fem fonder | Källprov | `README_SV.txt` |
| 3 nov | `omxsb_shof_coverage_20261103/` | SHoF:s täckning av fondhistorik | Avråder från att bygga huvudslutsatsen på den | Källprov | `README_SV.txt` |
| 3 nov | `omxsb_alternative_sources_20261103/` | Andra datakällor efter SHoF-begränsningen | Vägar finns; ingen mekanism löst | Källprov | `RESEARCH_NOTE.txt` |
| 3 nov | `omxsb_alternative_execution_20261103/` | LSEG-desktop (indexmedlemmar) och auktionspilot | Medlemmar verifierade, vikter saknas; två auktionskontraster med motsatta tecken | Källprov | `README_SV.txt` |
| 3 nov | `omxsb_scaled_round_20261103/` | Behåller nya fondägare positionen till nästa kvartal? | 0,831 → 0,973 pp för 59 tillägg | Utforskande | `README_SV.txt` |
| 3 nov | `omxsb_history_extension_20261103/` (+ `kod/`) | Händelser 2003–2006 | 54 med komplett fönster, preliminärt; huvudanalysen 2007–2026 oförändrad | Utforskande | `REPORT_SV.txt` |
| 3–4 nov | `omxsb_followthrough_20261103/` | Total omsättning kring tillägg (45 dagar) | +7,73 normala dagsomsättningar | Utforskande | `README_SV.txt` |
| 4 nov | `omxsb_shof_revisit_20261104/` | SHoF-källgranskning och första minutpilot | Delresultat, ersatt samma dag | Källprov, ersatt | `README_SV.txt` |
| 4 nov | `omxsb_source_and_overlap_20261104/` | Överlapp mellan nya fondpositioner och nästa rapport; SHoF-piloten slutförd | 83,12–96,90 % (70 tillägg 2019–2023) | Utforskande | `README_SV.txt` |
| 4 nov | `omxsb_design_reset_20261104/` | Omprövning av forskningsdesignen | Inga fler små varianter; ägarmätningen kan vara ett avgränsat mätbidrag men identifierar inte priset | Beslutsunderlag | `LAS_FORST.txt` |
| 4 nov | `omxsb_ad_research_20261104/` | Beskedsdatum för SBX/OMXSB 2003–2006 | NOREX-regelboken från 2005 hittad; inget av de åtta saknade datumen verifierat | Källprov | `REPORT_SV.txt` |
| 4 nov | `tabeller_och_figurer_20261104/` | Tabell 2, bilaga A1 och figur 1 i Word, från `claude_checks/tabeller_word.py` och `figurer.py` | – | Ersatt av `thesis_final/results/tables/` | `tabeller/LOGG.txt` |
| 10 nov | `thesis_final_2026-11-10.patch` | Alexanders patch (G&S urvalsregel för borttag) | Redan inarbetad i `thesis_final` (commit `6ce77b9`) | Ersatt | – |
| 2 nov | `PUBLICERING_20261102.txt` | Vilka filer som hölls lokala medan repot var publikt | De fyra filerna lades i git 13 nov (commit `1a9e54d`) | Historik | – |

Nästlade `.gitignore` i några paket (`private/`, `sources/`) gör att licensierade originalexporter ligger kvar på disk men inte i git. Så var det före 13 nov och det är oförändrat.
