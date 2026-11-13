OBEROENDE REPLAY AV LÅST BRUTTOOMSÄTTNINGSKONTRAST

Slutstatus: REPORT_SV.txt och FINAL_VALIDATION.json. verify.py gör inga nya
estimand och importerar inte producentens funktioner.

Krav: Python med pandas, numpy, scipy, pyarrow, xlrd. Licensierade original
måste finnas lokalt. Använd originalens SOURCE_GATE_LOCK och UNIT_GATE_SUMMARY
för exakta filer/hashar. Denna granskning kan inte köras från enbart publika
resultat eftersom den även kontrollerar originalpanelen och tio Nasdaq-xls.

Exempel:
python verify.py --repo-root /path/to/financethesis --work-root /path/to/work \
  --design /path/to/design --output /tmp/volume-audit-new.json

Ny --output krävs. Programmet skapar också en separat _LOCK.json och avbryter
om någon av dem redan finns. Originalkällor används via låsets paths när de
finns, annars söks motsvarande repo-/work-relativa paths. De tio månadsböckerna
söks i work/open_questions_20261101/eligibility/YYYYMM.xls om originalpath saknas.
xlrd kan vara installerat i Pythonmiljön eller i design/.deps. Inga bibliotek
eller data hämtas av granskningen. Frysta loggar ändras inte vid korrekt replay.

Publikation: exakt allowlist. PUBLICATION_SHA256 hashar alla listade filer utom
sig själv. Data/privata SEK-skalor, hela Nasdaq-filer, miljöer och producentens
privata export är uteslutna. Misslyckat första auditförsök bevaras öppet som
kod/logg/lås utan råbelopp; se REPORT_SV för den korrigerade NA-hanteringen.
