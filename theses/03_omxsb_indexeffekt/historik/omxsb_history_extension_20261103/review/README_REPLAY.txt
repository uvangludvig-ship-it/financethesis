HISTORIKGRANSKNING — REPRODUKTION

Slutstatus och begränsningar: REPORT_SV.txt. Kontrollresultat:
INDEPENDENT_VALIDATION.json. Detta paket innehåller inga licensierade prisnivåer.

Krav: Python med pandas, numpy, scipy, pyarrow. Rådata måste finnas lokalt under
licens och paths i analysens RUN_LOCK måste kunna lösas. Ingen ny hämtning görs.

Exempel (ersätt sökvägar):
python verify.py --repo-root /path/to/financethesis --output /tmp/history-audit-new.json

--results kan ange en alternativ kopia av den låsta resultatmappen. Default är
repo/output/omxsb_history_extension_20261103. --output kräver en ny fil, så den
frysta kontrollen skrivs inte över. --repo-root gör granskningen flyttbar; den
historiska standardsökvägen pekar på ursprungsrepot. Workbook-hash kan verifieras
mot den privata immutable user_source-kopian om ursprungliga Downloads saknas.

source_presence.py är den historiska första metadata-inventeringen. Dess
hardkodade repo och skydd mot att skriva över SOURCE_PRESENCE_LOCK bevaras som
ursprunglig kod; kör inte om den på plats. Slutreplay görs med verify.py.

Utdata redovisar bara antal, hashkontroller och numeriska differenser mellan
redan låsta resultat. Inga nya kontraster, prisutfall eller råserier exporteras.

Publikation: kopiera endast PUBLICATION_ALLOWLIST.json:s relativa filnamn.
PUBLICATION_SHA256.json hashar varje listad fil utom sig själv. Allt annat är
uteslutet, inklusive privata normaliserade uttag, hela arbetsboken, fullständig
medlemskatalog, eventuella miljömappar och dokumentfulltexter.
