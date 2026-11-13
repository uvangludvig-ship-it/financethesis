# Claude-kontroller, 1 november 2026: kod, indata och resultat

Allt här ska ligga i `code/claude_checks/`. Skripten körs från den mappen (`cd code/claude_checks`) och hittar repots rot som `../..`. Notebooks för hela panelen körs från repots rot, som tidigare.

## Bygg indata först (en gång)

1. `python3 fi_parse_all.py` läser alla FI-zippar i `data/raw/fi/` och skriver `data/fi_all_funds.csv` och `data/fi_all_holdings.pkl`. Pickle-filen (cirka 170 MB) ligger inte i paketet eftersom den är för stor; den byggs på några minuter.
2. `python3 fi_klass.py` skriver `data/fi_all_funds_klass.csv` (indexfonder, strikt och bred). Återskapar körningens klassning exakt.

Övriga indata i `data/`: `lseg_klassificering.csv`, `lseg_freefloat_hist.csv`, `lseg_saknade_aktier.csv` (hämtade med `runda2_lseg_CodeBook.ipynb`), `medlemskap_verifierad.csv`, `panel_utdrag.csv.gz` (186 aktier ur panelen) och `fi_check/` (äldre FI-utdrag för de första kontrollerna). Tvillingpriserna ligger redan i repot under `data/raw/lseg/twins/`.

## Skript i den ordning resultaten togs fram

| Steg | Skript | Deklaration | Resultat |
|---|---|---|---|
| Del 1, återgång | `del1.py` (med `common.py`) | `STRUKTUR_OMXSB.md` | `del1_results.csv`, `del1_events.csv` |
| Del 2, tvillingar | `twin_events.py`, `twin_prices.py`, `twin_prep.py`, `twin_core.py`, `twin_mde.py`, `twin_run.py`, `twin_explore.py` | `twin_excl_beslut.md` | `twin_results_*.csv` |
| Tilläggsanalyser A–D | `tillagg.py` | `tillagg_deklaration.md` | `tillagg_A_*.csv` |
| T1–T4 på utdraget | `robusthet.py` | `robusthet_deklaration.md` | `robusthet_*.csv` |
| T2-hela, T5 på hela panelen | `robusthet_hela.py` / `robusthet_hela_panelen.ipynb` (lokalt) | `robusthet_deklaration.md` | `hela_*.csv` |
| Medlemslistan | `medlemskap.py` | | `medlemskap_verifierad.csv`, `medlemskap_kontroll.txt` |
| Runda 2 (T5v, T6–T9, T11) | `runda2.py` = `runda2_lokal.ipynb` (lokalt, `INDATA=code/claude_checks/data`) | `runda2_deklaration.md` | `runda2_resultat/` |
| Runda 3 (T12, T13) | `runda3.py` = `runda3_lokal.ipynb` (lokalt) | `runda3_deklaration.md` | `runda3_resultat/` |
| A/B-revision | `ab_revision.py` | `ab_deklaration.md` | `ab_revision_*.csv` |
| Första steget v2 | `forsta_steget_v2.py` | `forsta_steget_deklaration.md` | `forsta_steget_v2_*.csv` |
| Runda 4 (T14) | `runda4.py 0`, `runda4.py 1`, `runda4.py 2` | `runda4_deklaration.md` | `runda4_resultat/` |
| Runda 5 (T15–T17) | `runda5_t15.py`, `runda5_t16_t17.py 1` / `2` | `runda5_deklaration.md` | `runda5_resultat/` |

Alla siffror och tolkningar finns i `RESULTAT_2026-11-01.md`.

Äldre kontroller och utforskning, inte del av huvudresultaten: `migration_check.py`, `split_others.py`, `window_check.py`, `parse_fi.py`, `recompute.py`, `gross_flows.py`, `lf_switch.py`, `lf_turnover.py`, `dropout_check.py`, `inspect_funds.py`, `twin_first_stage.py`, `twin_first_stage_active.py` (ersatt av första steget v2), `runda2_v1.py`, `runda2_lokalt_har.py`.

## Kända avvikelser

- Den breda definitionen av indexfonder tog med fonder utan uppgift om aktiv risk (107 av 957 fondkvartal). Se tillägget i `forsta_steget_deklaration.md`.
- `runda5_t15.py` och `runda4.py` är testkörda från den här mappstrukturen och ger samma siffror som i `RESULTAT`.
