Avgränsad genomförd analys,2026-11-02. Repo är oförändrat.

Läs REPORT.txt för resultat, källbegränsningar och tolkning.
GATE_PROTOCOL.txt skrevs före någon ny exponerings–prisassociation.
ANALYSIS_LOCK.json bevarar första analyslåsets tidsstämpel och exakta82event.

gate.py bygger preevent-exponering och officiell Nasdaq-likviditet utan nya prisutfall.
freeze_and_run.py låser urvalet och kör EN huvudmodell samt EN förutbestämd känslighet.
verify_raw.py jämför164endpointmängder med FI-rådata.

Kör från valfri katalog med:
/tmp/omxsb-audit-venv/bin/python /Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/deletion_exposure_20261102/gate.py
/tmp/omxsb-audit-venv/bin/python /Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/deletion_exposure_20261102/freeze_and_run.py
/tmp/omxsb-audit-venv/bin/python /Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/deletion_exposure_20261102/verify_raw.py

Nyckelfiler:
- gate_event_ledger.csv: alla97kanoniska borttag, samtliga skäl till15exklusioner.
- analysis_event_ledger.csv:82rader med exponering, föredata, källor, mängder, fryst kort prisutfall.
- results.csv: samtliga två förutbestämda modeller.
- quarter_liquidation_review_description.csv och quarter_liquidation_summary.json.
- raw_position_reconciliation.csv: granskning av alla164fond–värdepapper–datumpar.
- source_ledger.csv, source_hashes_gate.json, validation.json: proveniens/QA.
- pre_covariate_correlations.csv, exposure_residuals_NO_OUTCOMES.csv, review_exposure_information_share.csv.

Inga handelsdagsspecifika försäljningsbelopp, fullmarknadsmultiplikatorer eller kausala koefficienter påstås. Inga framtida100dagarsutfall har använts i denna analys.
