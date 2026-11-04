SHoF: närmare granskning av auktionsspåret, 4 november 2026
Teknisk arbetsrapport. Ingen uppsatstext och inga nya ekonomiska skattningar.

Det var detta spår användaren syftade på
Vi ville mäta priset i stängningsauktionen mot sista giltiga köp-/säljkurs
omedelbart före auktionen, på indexets handelsdag och på låsta jämförelsedagar.
Det säger hur priset ändras just när omviktningen genomförs. Det identifierar
inte ensamt orsaken till hela uppgången sedan indexbeskedet eller säljarens
identitet. De tidigare två 2023-exemplen är kvar som enskilda pilotfall.

Den tidigare flaskhalsen
LSEG:s kontrollerade auktionsfält gav täckning för två översyner 2023 men ingen
historisk täckning före 2023 i det låsta uttaget. SHoF gav sista orderbokskurs
före auktionen, men inte själva slutauktionen i de levererade filerna.
Detta stoppade den breda jämförelsen. Det bevisade inte att SHoF:s råarkiv
saknar stängningsauktionerna.

Vad vi nu har gjort och verifierat
1. Läst om samtliga sju bevarade SHoF-original. Fem fullböcker slutar mellan
   17:24:56 och 17:24:59 enligt exporterad klocka. Ingen har rader från17:25.
2. Bilia-uttaget Transactions innehåller exakt samma862 transaktionsrader
   som fullboken, med två kolumner borttagna:15 516 gemensamma celler lika.
   Det är ingen oberoende avslutskälla. NMQ-filen är dagsmått, inte minutdata.
3. Granskat aktuell SHoF-webb, äldre originalmanual och Nasdaq-protokollet.
   Manualen beskriver separata Trade Ticker och Full Day Timeserie. Råa
   Nasdaq-meddelanden har en särskild closing-cross-typ. Det ger en konkret
   annan källa att pröva, men dagens exporttillgång är fortfarande obekräftad.
4. Återkört hela råinventeringen och fått exakt samma metadata och filparbevis.
   Alla sju originalhashar är oförändrade. Inga råpriser publiceras.
5. Öppnat befintligt SHoF-formulär i Chrome och verifierat dess exportval.
   Vid navigering/omladdning skickade SHoF vidare till universitetsinloggning;
   den sidan visades tom. Användaren har fått en konkret begäran att återöppna
   exportformuläret via Handels. Inga nya datajobb har skickats denna runda.

Exakt nästa steg
Åtkomstkontroll av Trade Ticker/Full Day Timeserie med Bilia2019-05-31 och
Camurus2023-11-30. Kontrollera genomförd slutauktion, rättelser, identitet,
tidzon, prisskalning och matchnummer innan pris eller volym beräknas.
Om de separata produkterna saknas i den ordinarie menyn finns en specificerad
dataförfrågan att ta till SHoF. Den är inte skickad. Ingen produkt-URL gissas.

Separat behöver en skalbar export av kursen före auktionen valideras mot
befintliga fullböcker. Minut-/sekundaggregation är inte automatiskt sista
noterade kurs och återställer inte automatiskt saknade auktionsposter.
Den tidigare låsta valideringsordningen och dagens begränsning till högst
åtta källjobb finns i ACQUISITION_LOCK.txt. Hittills är antalet nya jobb0.

Vad detta betyder för uppsatsen
Spåret är fortfarande värt en avgränsad källkontroll. Får vi verkliga
auktionsavslut bakåt i tiden kan fler översyner bli möjliga att undersöka.
Det är ännu ingen ny empirisk upptäckt eller garanti om precision. Även en
fullgod auktionsfil visar handelsförloppet; den avslöjar inte automatiskt vilka
fonder/hedgefonder som handlar. Buyer/seller är tomt i alla fyra2023-fullböcker.
Tidigare breda stoppbeslut gäller tills faktisk täckning har verifierats.

Dokumentation: raw_audit/REPORT_SV.txt och documentation/REPORT_SV.txt.
Reproduktion: raw_audit/inventory.py; rotens kontroll: ROOT_REPLAY.json.
Alla äldre ekonomiska resultat är oförändrade. Ingen FTN-analys utförd.

ÅTKOMSTUPPDATERING 4 NOVEMBER 10.28 SVENSK TID
Användarens flyttmeddelande gäller databasens startsida. Via den officiella
nya webbplatsen, NASDAQ HFT -> Reconstructed Order Book -> Access the dataset,
öppnades exportformuläret åter på samma databasadress. Inloggning blockerar
inte längre den rekonstruerade produkten. Inga råproduktmenyer eller nya
exporter har därmed verifierats. Nya jobb är fortfarande0: fortsatt native
webbläsarstyrning avbröts upprepade gånger av samtidig användarnavigering.
Ingen aktivitet i användarens andra dokument; inga nya ekonomiska utfall.
