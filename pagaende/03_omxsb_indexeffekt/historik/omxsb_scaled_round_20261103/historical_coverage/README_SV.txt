OMXSB FÖRE 2007: LITEN GENOMFÖRD KÄLLPILOT
3 november 2026. Inga avkastningar, priser, vikter eller indexaktieantal.

Kort besked: möjligheten till äldre indexhistorik är inte motbevisad, men
den fungerande LSEG-frågan gav inga medlemmar på de tre provdatumen före
2007. Vi kan därför ännu inte bygga en äldre eventlista från dessa uttag.

Begärt datum    .OMXSBPI    .OMXSBGI    Tolkning
2000-12-29      tomt        tomt        Före faktisk SBX-lansering
2003-12-30      tomt        tomt        Ingen historisk medlemslista levererad
2006-12-29      tomt        tomt        Ingen historisk medlemslista levererad
2023-11-30      105         105         Positiv historisk medlemskontroll

Exakt åtta låsta get_data-anrop, med redan verifierade PI/GI-identiteter,
TR.IndexConstituentRIC och TR.IndexConstituentName samt SDate. De sex äldre
svaren var DataFrames med en instrumentrad och tomma medlemsfält. Det var
inga API-fel och inga bevis för noll faktiska medlemmar. De visar endast att
just dessa frågor i denna behöriga session inte levererade äldre innehåll.

Kontrollen gav 106 råa rader, varav 105 hade giltig unik RIC. Båda nya
kontrollmängderna är exakt lika den tidigare 2023-11-30-listan. De skiljer sig
från den redan sparade aktuella 111-medlemslistan med 42 RIC i symmetrisk
skillnad. Tidigare kontroll mellan 2023-11-30 och 2023-12-01 gav sex tillägg
och sju borttag, verifierade mot den slutliga Nasdaq-notisen efter
29 november-uppdateringen. Svaren har inget returnerat as-of-datum; SDate är
en förfrågeparameter. Ingen före-2007-lista eller historisk namntext har
därför certifierats som korrekt daterad. Inga extra datum/alias provades.

LIVE-LANSERING OCH HISTORISKT NAMN ÄR NU PRIMÄRKÄLLEBELAGDA
Stockholmsbörsens egen notis 2 juni 2003 anger att SBX, Stockholmsbörsens
Benchmark-index, lanserades 12 april 2001 och beräknas från 30 december
1995 med basvärde 100. Samma notis gäller starten för XACT SBX den 2 juni
2003; ETF-starten är alltså ett annat datum än indexlanseringen.
https://news.cision.com/se/stockholmsborsen/r/xact-sbx---en-ny-borshandlad-fond-noteras,c80505

OMX:s notis 22 augusti 2005 anger att Stockholms benchmark får namnet OMXSB
från 3 oktober 2005. SBX är belagt; SX Benchmark/SAXB har inte verifierats
som alternativa identiteter i denna pilot och användes inte i API-anrop.
https://news.cision.com/se/omx-exchanges/r/omx-harmoniserar-indexnamn,c161338

Historik från basdatumet före 12 april 2001 får inte behandlas som faktiska
historiska indexurval som marknaden reagerade på. Den ursprungliga
lanseringens första offentliggörande och initiala urvalsprocess är inte
utredda här. Indexstarten är inte automatiskt ett vanligt revisions-event.

VAD DATAN SKULLE KUNNA GE — OCH INTE GER HÄR
Daterade, validerade medlemslistor före/efter en förändring kan hjälpa
identifiera inträden/utträden och avgränsa ett implementeringsdatum. För
exakt effektivdag behövs tillräcklig datumupplösning och rätt SOD/EOD-
konvention; årsvisa snapshots räcker inte. En viktförändring ensam kan vara
prisdrift eller en företagshändelse och identifierar inte en indexrevision.
Ingen sådan förändring har beräknats i piloten.

Annonseringsdatum kan inte räknas bakåt från medlemskap/vikter utan en
samtida verifierad regel eller daterad originalnotis. Nuvarande schema får
inte antas gälla 2001–2006. Tidigare projektarbete dokumenterar dessutom
januari/juli-implementering till januari 2009, före juni/december-regimen.

PRAKTISK GRÄNS OCH REPRODUKTION
Om äldre medlemskap behövs är den precisa återstående innehållsfrågan om
LSEG kan leverera historiska constituents för den daterat verifierade
SBX/OMXSB-kedjan 2001–2006 via annan dokumenterad leverans. Det är inte
klarlagt av dessa tomma svar; ingen alias-/fältmatris, kontakt eller köp har
gjorts. Originalnotiser krävs fortfarande för en säker AD-eventstudie.

pilot.py och PILOT_LOCK.json visar hela låsta uttaget. validate.py jämför
med redan sparade källkontroller; VALIDATION.json redovisar begränsningarna.
PILOT_RESULTS.json innehåller bara status, antal och hashvärden. Råmedlemmar,
namn och fullständiga primärkällor ligger i private/ och får inte publiceras.
PUBLICATION_ALLOWLIST.json är en exakt JSON-lista med relativa filnamn.
PUBLICATION_SHA256.json hashar alla tillåtna filer utom hashmanifestet självt.
Den lokala SDK-sessionen stängdes; Workspace loggades inte ut. Inga repoändringar.
