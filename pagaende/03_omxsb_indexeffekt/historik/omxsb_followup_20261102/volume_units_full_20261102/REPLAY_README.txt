Portabel tilläggsreplay — volume_units_full_20261102

Kopiera de två katalogerna med samma relativa sökvägar till repo:
code/build/omxsb_followup_20261102/volume_units_full_20261102/
output/omxsb_followup_20261102/volume_units_full_20261102/

Kör från valfri katalog:
python REPO/code/build/omxsb_followup_20261102/volume_units_full_20261102/replay.py --repo REPO
Alternativ outputrot anges med --output ROT; hela denna volymkatalog med sparade filer måste då finnas under ROT/volume_units_full_20261102.

Körningen läser den bytebevarade, låsta205-grinden och råpanelens volymfält och tillämpar enbart de frysta associationerna. Den bygger aldrig en ny enhetsgrind. Nytt mandate-underlag följer med som inputs/event_demand_updated.csv med exakt källa/hash, så ingen separat agents ännu ej kopierade katalog krävs. Övriga fyra frysta repo-indata verifieras mot PORTABLE_INPUT_MANIFEST innan körning. Ingen nätanslutning eller ny hämtning krävs. Python behöver numpy, pandas, scipy, statsmodels och pyarrow.

Fem vetenskapliga resultatfiler jämförs mot archived_original_work; alla lås, fördeklarationer, originalkod och originalrapporter bevaras byteidentiska. Ursprungskod och historiska källfält innehåller avsiktligt de ursprungliga lokala sökvägarna som proveniens, men den aktiva associationskoden använder portabla sökvägar. frozen_fieller.py innehåller exakt samma funktionskod som originalet, inte en omskriven metod. path_only_code_changes.diff visar alla ändringar av den aktiva koden.

Utförd lokal portabel replay: alla fem CSV-resultat är byteidentiska, max numeriskt fel0. Original172, common166 och corrected205 finns samtliga kvar i kvottabellen. Se PORTABLE_REPLAY_VALIDATION.json. Denna tilläggsreplay är separat från den befintliga överordnade replay.py; inget gammalt pakets schema har ändrats.
