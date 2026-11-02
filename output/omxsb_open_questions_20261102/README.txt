OMXSB: faktisk omkörning och datagranskning, 1–2 november 2026

Börja med RESULTAT.txt. Det är tekniskt arbetsunderlag, inte färdig uppsatstext.

Viktigaste filer
eligible_rematch/results.csv: ommatchning med daterade huvudlistekontroller; senaste och källmässigt starkaste av de körda matchningarna, men fortfarande en observationsjämförelse och en ofullständigt länkad kandidatpool.
eligible_rematch/event_paths.csv och selected_controls.csv: varje händelse, förvalda kontroller och samma fyra horisonter.
eligible_rematch/validation.json: oberoende kontroll av samtliga 287 matchningar och 18 resultatrader.
demand_quarter/summary_review_weighted.csv: kvartalsvisa positiva/negativa fondnetton och nettot, på samma 216 händelser.
demand_quarter/root_independent_numeric_check.json: separat avstämning av 24 skattningar och intervall från fondraderna.
eligibility/:19 ursprungliga Nasdaq-arbetsböcker,19 meddelanden, exakta URL:er, källhashar och publiceringstider.
eligible_pool/: strikt historiskt listad och identifierarlänkad kandidatpool. Olösta instrument ingår inte som bevisade icke-kandidater.
eligibility_links/: granskning av de tidigare fasta matchningarna, inklusive den separat redovisade 69-händelsekänsligheten. invalid_join_attempt är en dokumenterad felkoppling som INTE används som ett ekonomiskt resultat.
persistence/ och persistence_corrected/: tidigare deklarerad körning och rättelse av två egenkontroller. Dessa resultat är bevarade, inte utplånade av ommatchningen.
persistence_validation/: oberoende rådatareproduktion, identitetskontroll och frysta ursprungsfiler.
independent/: A/B:s gemensamma kvotosäkerhet, styrkegrindar och H-dataproblem. Ingen osäker H-regression har körts.
retention/: fonders fortsatta positiva position vid nästa kvartal; mängd-/ägarandelsgrinden är blockerad och inga sådana kvoter används.
price_path.png och price_path.pdf: den senaste daterade kontrollkörningen,135 gemensamma tillägg över alla horisonter.
ANALYSIS_LEDGER.txt: alla genomförda steg, inklusive resultat som inte blev tydliga.

Körning i det befintliga repot
Kräver Python med numpy,pandas,scipy,statsmodels,pyarrow; Excelvalidering även openpyxl och xlrd. Ett fungerande lokalt Python är /tmp/omxsb-audit-venv/bin/python. Full prisparquet, FI-derived och tidigare granskade ownership-utdata måste finnas; ZIP-filen duplicerar inte hela dessa stora indata. De anges med hash i respektive metadatafil.

Huvudresultat från rå prispanel och den sparade daterade poolen:
python output/omxsb_open_questions_20261102/eligible_rematch/run.py

Kvartalsdekomposition från befintliga råa FI-derived och den granskade halvårs-/identitetskedjan:
python output/omxsb_open_questions_20261102/demand/denominator_audit.py
python output/omxsb_open_questions_20261102/demand/describe_fund_changes.py
python output/omxsb_open_questions_20261102/demand_quarter/gate.py
python output/omxsb_open_questions_20261102/demand_quarter/resolve_gate.py
python output/omxsb_open_questions_20261102/demand_quarter/describe_quarter.py

Återhämta/verifiera Nasdaq-original:
python output/omxsb_open_questions_20261102/eligibility/fetch_verified_sources.py
python output/omxsb_open_questions_20261102/eligibility/validate_sources.py

När paketet ligger någon annanstans än repo/output kan miljövariabeln FINANCETHESIS_REPO sättas till repots absoluta sökväg. Annars hittar paketerade huvudskript repot från sin placering. Arkiverade originalskript är bevarade utan sökvägsändringar. PACKAGING_CHANGES.json beskriver enbart portabilitetsändringar och den uttryckligen medpaketerade H-metadatafilen. Hämtningsskript använder publika källor; ingen LSEG-session startas av dessa körningar.

Körningar skriver i respektive analysmapp. Kopiera mappen först om även levererade maskinmetadata/hashar ska ligga helt frysta. Originaldata ändras inte. MANIFEST_SHA256.json listar levererade filer; ZIP-manifest finns även utanför ZIP-filen.

Väsentliga begränsningar
Main-market Stock-screen är inte fullständig OMXSB/OMXSPI-behörighet eller slumpmässig tilldelning.19 översyner är få oberoende block, företag återkommer, sena avkastningar kräver komplett täckning och kontroller kan drabbas av andra nyheter. Fondnetton per kvartal identifierar inte handelstidpunkt eller motpart. Tidigare resultat var kända före följdanalyserna. Nominella p-värden ska inte tolkas som om hela arbetet bestod av ett enda blint test.

Inget nytt har pushats automatiskt. Befintliga ocommittade projektändringar har bevarats. Inga FTN-avkastningar eller manuskriptavsnitt har producerats.
