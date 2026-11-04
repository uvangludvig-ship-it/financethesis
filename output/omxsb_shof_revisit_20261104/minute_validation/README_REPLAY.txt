BILIA MINUTPILOT — DELRAPPORT FÖRE ÅTERSTÅENDE LEVERANSER

Läs BILIA_SOURCE_NOTE.txt. BILIA_BIN_ORDERING_CHECK.json är den slutliga oberoende
bucketjämförelsen och BILIA_PREDECLARED_VALIDATOR.json den tidigare fastställda
validatorns körning. Fyra övriga fasta pilotdagar är uttryckligen pending/missing,
inte misslyckad tillståndslikhet eller saknade auktioner i hela databasen.

Rå leverans och jämförelsebok måste finnas lokalt under licens. Inga råvärden
finns i detta publiceringspaket. BILIA_MINUTE_ACQUISITION.json anger exakta
inputhashar och metadata. Den nya råkopian ligger i ignored hft_revisit_20261104.

Oberoende replay kräver bara Python-standardbiblioteket:
python compare_bins.py --repo-root /path/to/financethesis \
 --input /path/to/financethesis/data/raw/shof/Reinvestments/hft_revisit_20261104/NASDAQ_2nd_level_orderbook_1793788245204.csv.zip \
 --out /tmp/bilia-minute-new.json

Ny --out krävs; en existerande resultatfil skrivs aldrig över. Fullfilens
relativa path är fördefinierad under repo-root. Scriptet behandlar bara de fem
redan låsta pilotdagarna. Eventuella extra rangedagar listas men jämförs inte.
Kronologi och tvetydiga likatidsslut kontrolleras innan sista-radstolkningen.
Priser/storlekar används bara för likhetskontroll med fixerad tolerans1e−10;
inga nivåer, medelpriser, VWAP, volymsummor, returer eller premier exporteras.

Fördeklarerad validator finns redan i repot:
output/omxsb_scaled_round_20261103/auction_design/validate_sampled_export.py
med SAMPLING_VALIDATION_SPEC.txt i samma mapp. Kör den med samma --input,
--interval minute och en ny --out. Den behöver pandas/numpy och använder den
ursprungliga fasta fullboksmappen. Hashar finns i förvärvs-/validator-JSON.

Notera två olika fakta: originalets nanosekundstid bevaras INTE i sample, men
fullboken belägger actual update inom sista60sekunderna för Bilia. Global
färskhet eller femdagarsgodkännande hävdas inte. Inget ytterligare sekunduttag
görs enbart för att minutetiketten är rundad.

PUBLICATION_ALLOWLIST.json är exakt. Manifestet hashar alla listade filer utom
sig självt. Alla licensierade råfiler och äldre lokala arbetsversioner utesluts.
Tidigare egna bucketkörningar bevaras lokalt. Slutkoden tillför uttrycklig
kronologi-/tie-kontroll och en generell lista över eventuella extra minuter.
Alla tidigare likhets- och täckningsresultat för Bilia är oförändrade.
