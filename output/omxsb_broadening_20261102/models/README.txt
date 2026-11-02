Reproduktion i samma projektmiljö:
/tmp/omxsb-audit-venv/bin/python work/broadening_models_20261102/prepare.py
/tmp/omxsb-audit-venv/bin/python work/broadening_models_20261102/compare.py
/tmp/omxsb-audit-venv/bin/python work/broadening_models_20261102/verify.py

För granskning ska de sparade DECISIONS, DESIGN_LOCK och feature_gate_all216 bevaras; prepare räknar om grinden och är därför inte del av en fryst replay. compare kan köras direkt mot sparad grind. Ingen fil utanför denna katalog skrivs av dessa tre script. Inga FTN-filer läses. Originalkällor och tidigare resultat förblir oförändrade. Detta är internt analysunderlag, inte uppsatstext.
