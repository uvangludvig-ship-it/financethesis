FORTSÄTTNING EFTER HISTORIKUTÖKNINGEN, 3–4 NOVEMBER 2026
Tekniskt resultat- och beslutsunderlag, inte uppsatstext.

DET NYA TESTET
En hög andel av periodens handel på indexdagen kan uppkomma på två sätt:
mer handel på indexdagen, eller mindre handel på övriga dagar. En volymandel
som alltid summerar till100 procent kan inte ensam skilja detta åt.

Vi mäter därför omsättningen i kronor på handelsdagen och övriga44 dagar,
var och en relativt aktiens egen tidigare normala dagsomsättning. Sedan
drar vi av samma mått för exakt tre tidigare frysta kontrollaktier.
Det ger en exakt uppdelning: hela45-dagarsperioden = handelsdagen + övriga dagar.
De tre delarna använder alltid samma bolag, jämförelseaktier och tidsfönster.

URVAL OCH KÄLLOR
70 tidigare fastlagda tillägg2019–2023 och tre kontroller per tillägg var startpopulationen.
65 set på10 översyner har fullständig data och klarar enhetskontrollen.
Före resultaten stämdes LSEG:s dagliga TR.Turnover av mot tio Nasdaq-original
på månadsnivå.245 av250 unika månad/aktie-kontroller godkändes. De fem
underkända motsvarar redan saknade datapunkter; inga utfall användes för urvalet.
50 referensdagar före beskedet överlappar aldrig45-dagarsfönstret runt bytet.
Det är bruttohandel i SEK på den täckta handelsplatsen, inte nettoköp eller antal aktier.

RESULTAT
Mått: skillnad mot kontroller, uttryckt i respektive akties normala dagsomsättningar.
Lika vikt för händelser inom översyn och sedan lika vikt för de tio översynerna.

Hela45-dagarsperioden: +7,73; nominellt95%-intervall [0,08;15,37].
Handelsdagen ED−1:    +5,53 (beskrivande del).
Övriga44 dagar:       +2,20 (beskrivande del).

Punktskattningen visar alltså ingen fullständig motverkande minskning under
de andra44 dagarna. Skillnaderna mellan översyner är stora: vissa har lägre
total relativ aktivitet trots en positiv handelsdagstopp. Samtliga tio översyner
redovisas i activity/REVIEW_COMPONENTS.csv och i TRADING_ACCOUNTING.png.

HUR STARKT ÄR BESKEDET?
Intervallet är brett och dess nedre gräns ligger mycket nära noll. Det är ett
explorativt, nominellt intervall efter omfattande tidigare analyser, inte ett
starkt bekräftande test. Återkommande bolag, gemensamma marknadslägen och
valda kontrollaktier begränsar antagandet om oberoende översyner.
Högre aktiekurser ökar också omsättningen i SEK vid oförändrat antal handlade aktier.
Aktivitet kan ha flyttats från dagar utanför det valda fönstret.

Detta identifierar därför inte indexköpens storlek, motparter, prisets orsak,
arbitragevinster eller en bestående förändring av handeln. Kontrollaktierna
kan själva påverkas av andra index och nyheter. Urvalet valdes ursprungligen
för ägardatans täckning och är inte alla svenska tillägg.

VARFÖR DET ÄNDÅ TILLFÖR NÅGOT
Testet kompletterar er tidigare volymandel med ett mått på samlad relativ
handelsaktivitet. Det hindrar att en större handelsdagsandel automatiskt
tolkas som större nettoköp eller bara omfördelad handel. Använd det som en
avgränsad komplettering, inte som en lösning på prismekanismen.

LITTERATURKONTROLL
Fyra närliggande original granskades. Handelsdagstoppar och volym relativt
en extern referensperiod är redan etablerade i forskningen; ingen ny generell
metod eller mekanism hävdas. Se literature/REPORT_SV.txt. Där skiljs också
Greenwood–Sammons2023- och2024/JF2025-versioner och deras olika figurnumrering.

YTTERLIGARE KÄLLFYND
AP7:s originalrapport för2002 dokumenterar indexförvaltning inom svenska
aktier och SBX som jämförelseindex från1 augusti2002. XACT SBX:s start2003
kan därför inte behandlas som starten för all efterfrågan kopplad till SBX.
Endast en av våra åtta tidiga kandidatöversyner ligger före ETF-starten.
Ingen kausal studie av ETF-starten körs på detta underlag. Se institutional/REPORT_SV.txt.

VERIFIERING OCH FILER
Oberoende rårekonstruktion: PASS. Alla280 stödroller,250 månadskontroller,
24700 exporterade råvärden och samtliga roll-/event-/översynskomponenter
och huvudresultat återskapas. Ingen ny FTN-analys och inga ändrade äldre resultat.

activity/: specifikation, källgrindar, ett huvudtest, alla komponenter och körkod.
independent_audit/: separat rårekonstruktion, resultat och publiceringsgränser.
institutional/: källtidslinje och varför ETF-starten inte används som experiment.
literature/: närmaste litteratur och begränsning av bidragets nyhet.
Licensierade råbelopp och fullständiga tredjeparters texter publiceras inte.

Historikutökningens samtliga periodresultat finns separat i
../omxsb_history_extension_20261103/FULL_PERIOD_RESULTS.csv och REPORT_SV.txt.
Tidiga händelser där är fortsatt preliminära, inte nya verifierade beskedstester.
