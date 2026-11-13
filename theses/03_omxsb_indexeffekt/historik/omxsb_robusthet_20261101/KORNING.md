# Körning och vad som valideras

Rättelse efter kända resultat, version5. Inga FTN-utfall eller rådata ändras.

Kör från repot med Python och beroendena i requirements.lock. I denna granskning användes /tmp/omxsb-audit-venv/bin/python.

1. python code/build/test_robusthet_repair.py
2. python code/claude_checks/test_twin_first_stage.py
3. python code/claude_checks/twin_first_stage.py --repo . --output-dir output/omxsb_robusthet_20261101/first_stage_validation
4. python code/build/robusthet_hela.py
5. python code/build/validate_robusthet_repair.py
6. python code/build/finalize_robusthet_repair.py

Steg3 skriver metadata/NA och returnerar avsiktligt exitkod2 när förstastegets underlag är ofullständigt. Det är inte ett ekonomiskt nollresultat och ska inte döljas som lyckad skattning. Fortsätt med den oberoende kontrollanalysen i steg4. Kör inte hela listan med ett villkor som kräver exit0 från valideringsspärren.

Rootens robusthet_hela.py är kompatibilitetsstart; notebooken anropar samma kanoniska analyskod. Den sista paketeringen lägger även till valideringsresultat, testkod och dokumentation i robusthet_hela_resultat.zip.

Valideringen jämför samtliga T2-medel och intervall med statsmodels, kontrollerar matcher, tidsgränser och NA-status, och bekräftar att450 gemensamma event-CAR är oförändrade mot den föregående exporten. Tio inferens-/urvalstester och fyra förstastegstester passerar. Det verifierar implementationen, inte en kausal design.

Original i archive/robusthet_repair_20261101/. Gamla robusthet_hela_resultat/ är markerad SUPERSEDED. Aktuella tabeller ligger i denna mapp. Primärtabellen results.csv innehåller explicita spärrade T5-rader; tolka inte saknade skattningar som0.
