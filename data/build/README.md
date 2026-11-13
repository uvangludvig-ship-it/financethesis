# data/build/: koden som bygger eller hämtar data

Här ligger all kod som skriver till `data/raw/`, `data/input/` eller `data/derived/`. Till 13 nov 2026 låg den i `code/build/` och `code/lseg/`. Analyskod ligger i respektive uppsatsmapp under `theses/`.

Skripten hittar repots rot med `../..` från sin egen plats. De ligger på samma djup som förut och fungerar därför oförändrat. Två rader ändrades 13 nov eftersom de pekade på flyttade resultatmappar: `omxsb_map_ric_2007_2012.py` och `lseg/tvilling_data.py`.

| Fil | Bygger | Från | Alternativ |
|---|---|---|---|
| `omxsb_build.py` | `data/input/omxsb/omxsb_changes_2013_2026.csv` (394 händelser) | Nasdaqs besked, källor i `omxsb_notes.md` | 03 |
| `omxsb_build_2005_2012.py` | `data/input/omxsb/omxsb_changes_2005_2012.csv` (142 händelser) | OMX/Nasdaq OMX-besked, `omxsb_notes_2005_2012.md` | 03 |
| `omxsb_map_ric_2007_2012.py` | `data/input/omxsb/omxsb_changes_2007_2026.csv` och `omxsb_events_with_ric_2007_2026.csv` (536 händelser med RIC). Granskningsfilen skrivs till `theses/03_omxsb_indexeffekt/historik/omxsb_replication_2007/mapping_review.txt` | de två listorna, `panel_2005_2026` | 03 |
| `omxs30_build_csv.py` | `data/input/omxsb/omxs30_changes_2005_2026.csv` (48 händelser) | `omxs30_notes.md` | 03 |
| `parse_ap_20261031.py`, `collect_ap_fi_20261031.py`, `finalize_ap_fi_20261031.py` | Hämtar AP-fondernas innehavslistor och FI:s blankningsregister till `data/raw/ap/` och `data/raw/fi_short/`, och bygger `data/derived/ap/` | AP1–AP4:s webbplatser, FI | 03 (historik) |
| `build_ppm_panel_2018.py` | `data/derived/ppm/ppm_panel_2018_2026.csv` | `data/raw/ppm/` | 01, 02 |
| `build_ppm_panel_2022.py` | `data/derived/ftn/ppm_panel_2022_2026.csv` | `data/raw/ppm/2021-2026/` | 02 |
| `detect_exit_days.py` | `data/derived/exit_days/` (förlorarnas tranchdagar, inga avkastningar) | `data/raw/shof/Valuations/` (delas för hand), rundmedlemskap, korsnyckel | 02. Körs om efter varje SHoF-uppdatering |
| `swing_build_outputs.py` | `data/input/swing/*.csv` | rundmedlemskap, PPM-panelen, fonddokument | 02. Läser `purge2019_candidates.json`, som inte finns i repot |
| `shof_monthly.py` | `data/derived/shof_monthly/` | SHoF:s dagliga exporter | 02. Sökvägarna i skriptet är från datorn där det kördes |
| `agent_runs/` | `data/derived/measurements/`, `data/derived/facts/` | | 01, 02. **Arkiv:** skrivna av agenter i oktober med absoluta sökvägar. Sparade för spårbarhet, går inte att köra som de är |
| `lseg/lseg_pull_v4.py`, `.ipynb` | `data/raw/lseg/panel_2012_2026/`, `panel_2005_2026/`, `panel_eu/` | LSEG Workspace CodeBook (körs där, inte lokalt) | 02, 03. `lseg/old/` innehåller v1–v3 |
| `lseg/tvilling_lseg_CodeBook.ipynb`, `tvilling_lseg_fix.ipynb` | `data/raw/lseg/twins/` | LSEG Workspace CodeBook | 03 |
| `lseg/tvilling_data.py`, `del1_panel_lokalt.ipynb` | Panelutdraget `panel_utdrag.csv.gz` (körs lokalt från repots rot) | `data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet` | 03. Utdraget används nu som `thesis_final/data/prices/stock_prices_daily_2004_2026.csv.gz` |
