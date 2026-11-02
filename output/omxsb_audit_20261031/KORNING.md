# Reproducera OMXSB granskningen

Kör från reporoten på Python 3.14.7 (miljön som användes). `requirements.lock` låser de faktiskt installerade versionerna. Paketen kan installeras i annan Python-version endast om motsvarande versioner stöds. Inga FTN-skript ingår.

```sh
python3 -m venv /tmp/omxsb-audit-venv
/tmp/omxsb-audit-venv/bin/pip install -r output/omxsb_audit_20261031/requirements.lock
git lfs pull
export MPLBACKEND=Agg
export MPLCONFIGDIR=/tmp/omxsb-audit-matplotlib
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_inputs.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_fi_raw.py
/tmp/omxsb-audit-venv/bin/python code/build/test_omxsb_audit.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_run.py baseline --periods
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_run.py corrected --periods
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_candidates.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_results.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_report.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_finalize.py
```

`git lfs pull` hämtar objekt men verifierar inte att deras interna format är oskadat. Inputskriptet läser parquet och FI, testar zip/CRC och jämför LFS-hash. CRC-felet i stocks_daily_2005.csv.gz är känt och ska kvarstå som dokumenterat fel; analysen använder parquet. Inputskriptet skriver en status per fil, så läs inventeringen och stoppa analysen om andra nödvändiga indata är oläsbara.

Baseline använder koden och exporterna från den frysta committen b886f5b744f797a6c1252f0e41fe2b740591c8c3. Om snapshoten saknas återskapas den från git-objekten i just den committen, inte från aktuell korrigerad kod. Alla kodceller körs; ingen cachad notebookutdata återanvänds. Endast exportvägarna omdirigeras. Mekanism-, period- och trendskript körs efter notebooken. Originalets filordning från Python-mängder kan variera; jämförelsen sorterar på nyckel. Baseline behåller det ursprungliga bootstrap-tieproblemet av reproduktionsskäl.

`corrected/` är den korrigerade analysen. Äldre exporter i `output/omxsb_replication_2007/` och originalsnapshoten ändras inte. Notebookens gamla inbäddade outputs är rensade för att undvika att de visas som om de hörde till rättad kod; fulla körloggar och nya exporter levereras. Vanlig interaktiv körning av notebooken skriver fortfarande till den äldre standardkatalogen, så använd audit-köraren för bevarad jämförelse.

Nasdaq-provfilen finns i paketet. För oberoende nyhämtning:

```sh
curl -L --fail 'https://attachment.news.eu.nasdaq.com/a8cb43b3dac4a07770fd3957b8858b42a' -o /tmp/nasdaq_202002.xls
shasum -a 256 /tmp/nasdaq_202002.xls
```

Förväntad SHA256: b7cd6b69eae58b19d5ff465dfa0afbaa0fa30da49aa091492b7790eeb753860a. Filen är publicerad 23 mars 2020. Oktoberfilerna ingår inte. `candidate_pilot_targets.csv` listar bara mål för framtida kontroll och kör inga nya avkastningstest.

De tre splitkällorna i split_source_verification.csv och licens-/åtkomststatus i data_gaps.csv är manuellt verifierad dokumentation från 31 oktober 2026. De återskapas inte genom analyskörningen. Full extern historisk datatäckning, fondöverföringar och mandat är uttryckligen inte verifierade.
