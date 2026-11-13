# arkiv/repo_historik/

Repots egen historik, det som inte hör till ett enskilt uppsatsalternativ. Fram till 13 nov 2026 hette mappen `archive/`. Samma dag flyttades det mesta som låg här till respektive alternativ:
- `topic_selection_2026-09/`, `agent_reports/`, `synopsis_source/` och `tmp/winner_review/` → `arkiv/00_amnesval_sep2026/`
- `research_archive/`, `literature_sweeps_2026-10/` och `tmp/anchor_audit/` → `arkiv/01_ftn_tidiga_ankare_okt2026/`
- `summaries_2026-10/` → `arkiv/02_ftn_pristryck_gs_okt2026/`
- `robusthet_repair_20261101/` och `omxsb_extension_20261031/` → `pagaende/03_omxsb_indexeffekt/historik/`

| Fil eller mapp | Vad |
|---|---|
| `FLYTTKARTA_2026-11-13.tsv` | **Varje fil som fanns före 13 nov 2026 och har flyttats:** gammal sökväg, ny sökväg, md5, storlek och om filen låg i git. 4 391 rader. Flytten gjordes i två steg samma dag och verifierades med md5 före och efter båda; ingen fil saknades och ingen ändrades av flytten. Kartans md5 är innehållet före 13 nov. Nio filer ändrades avsiktligt efter flytten och har därför ett annat innehåll i dag:<br>- `AI_LOG.md` (ny rad)<br>- denna README (förr `archive/README.md`)<br>- `thesis_final/README.md` (en sökväg)<br>- `data/build/omxsb_map_ric_2007_2012.py` och `data/build/lseg/tvilling_data.py` (en rad var)<br>- fyra skript i `arkiv/02_ftn_pristryck_gs_okt2026/kod/` (repo-rot och utmapp) |
| `old_readmes/` | Startsidor och README-filer från mappar som inte finns längre: rotens README fram till 4 nov (`README_rot_2026-11-04.md`), `thesis/README.md` och `code/README.md` från 27 okt, samt READMEs för `thesis2/` från 12–25 okt |
| `inventory/` | `DATA_INVENTORY_2026-10-26.md` (maskingenererad profil av varje datafil 26 okt) och `STRUKTUR_2026-10-27.md` (inventeringen bakom omstruktureringen 27 okt) |
| `course_text_extracts/` | Textutdrag ur kursplanen, introduktionsföreläsningen och synopsisinstruktionen (härledda kopior; originalen ligger i `reference/course_context/`) |
| `tmp/pdfs/` | Arbetsfiler från ämnesvalet: textutdrag ur ekonometrimaterialet och två sidbilder av synopsisen |
| `duplicates/` | Byte-identiska kopior av filer som finns på ett annat ställe. Tabellerna nedan anger var originalet finns |

## duplicates/

| Fil här | Identisk med (originalet) |
|---|---|
| `codebook_isin_list_lseg.csv` | `data/input/lseg/isin_list_lseg.csv` |
| `codebook_omxsb_changes_2013_2026.csv` | `data/input/omxsb/omxsb_changes_2013_2026.csv` |
| `drive-download-20261025T185638Z-1-001_same_as_panel_2012_2026.zip` | de fem filerna i `data/raw/lseg/panel_2012_2026/` |
| `extra_ppm_2023_12.xlsm`, `extra_ppm_2024_03.xlsm`, `extra_ppm_2024_06.xlsm`, `extra_ppm_2026_06.xlsm`, `extra_ppm_2026_08.xlsm` | samma månader i `data/raw/ppm/2021-2026/` |
| `root_code_ipynb_empty_placeholder.ipynb` | en tom notebook på 602 byte som låg i roten; den riktiga är `pagaende/03_omxsb_indexeffekt/historik/omxsb_replication/kod/replication_omxsb.ipynb` |

### duplicates/20261113_rot/ (låg i repots rot fram till 13 nov 2026)

| Fil här | Identisk med (originalet) |
|---|---|
| `panel_utdrag.csv.gz` | `pagaende/03_omxsb_indexeffekt/thesis_final/data/prices/stock_prices_daily_2004_2026.csv.gz` och `pagaende/03_omxsb_indexeffekt/historik/claude_checks/data/panel_utdrag.csv.gz` |
| `RESULTAT_2026-11-01.md` | `pagaende/03_omxsb_indexeffekt/historik/omxsb_robusthet_20261101/RESULTAT.md` |
| `robusthet_hela_panelen.ipynb` | `pagaende/03_omxsb_indexeffekt/historik/omxsb_robusthet_20261101/kod/robusthet_hela_panelen.ipynb` |
| `runda2_resultat/` (44 filer) | `pagaende/03_omxsb_indexeffekt/historik/claude_checks/runda2_resultat/` |
| `runda3_resultat/` (3 filer) | `pagaende/03_omxsb_indexeffekt/historik/claude_checks/runda3_resultat/` |

Dubbletter som fick ligga kvar eftersom båda kopiorna läses av kod eller hör till en sammanhållen helhet:
- `data/derived/measurements/` delar fyra filer med `data/derived/ftn/`, och 20 filer där finns också i `arkiv/01_ftn_tidiga_ankare_okt2026/research_archive/revised_2026-10-11/data/`.
- Indatapaketet `pagaende/03_omxsb_indexeffekt/historik/claude_checks/lokal_korning_rot_20261101/runda2_indata/` innehåller kopior av LSEG-filerna i `data/raw/lseg/klassificering/` och av `medlemskap_*` och `runda2_deklaration.md` i `claude_checks/`.
- `pagaende/03_omxsb_indexeffekt/historik/omxsb_robusthet_20261101/rot_20261101/robusthet_hela_resultat/` innehåller fyra filer som också finns i `robusthet_repair_20261101/` och i `claude_checks/` (`hela_*`).
- `pagaende/03_omxsb_indexeffekt/thesis_final/data/` är en avsiktlig fryst kopia av sina källfiler, se `thesis_final/data/FILES.csv`.
