Ny ägarmätning och slutförd SHoF-pilot, 4 november 2026
Teknisk resultat- och leveransnot. Inte uppsatstext.

NYTT EMPIRISKT BESKED
Vid nästa kvartalsrapport motsvaras 83.12–96.90 procent av den
ursprungliga nya fondkohortens positionsstorlek av innehav i samma fond
och aktie. Alla 70 frysta OMXSB-tillägg 2019–2023 och 10 översyner ingår.
Varje aktie vägs lika inom översyn och varje översyn lika. Det är inte en
poolad andel investerade kronor, en andel indexfondsköp eller en priselasticitet.

För varje fond begränsas bidraget till den ursprungliga positionens storlek.
Växande innehav hos en fond kan därför inte maskera krympande innehav hos en
annan. Samtliga ursprungliga positioner ligger kvar i nämnaren. Okänt senare
innehav ges hela intervallet noll till ursprungsstorleken, inte ett punktvärde.
737 ursprungliga fond–aktie-positioner ingår, varav 617 har samma godkända
källstöd som i den tidigare F35-analysen. 57 event har helt stöd, två delvis
och elva helt okänt senare stöd. De elva tas inte bort.

Gränserna gäller det observerade urvalet och de granskade mätreglerna.
De är INTE ett konfidensintervall. Rapporterad frånvaro av en aktie i en
närvarande, identifierad fondrapport räknas som noll enligt den gamla regeln.
Det gäller 35 positioner. Kontroll av rapportnärvaro är inte en extern
garanti för att varje rapport innehåller alla korrekta innehav. Gränserna
täcker inte fel i ursprunglig kohort, q1-vikter, identiteter eller mätningar.
SOURCE_RULE_INTERPRETATION_NOTE.txt i next_test preciserar detta.

VARFÖR MÄTA DETTA?
Den tidigare analysen mätte nettot över hela den nya ägarkohorten.
Ett sådant netto kan dölja att vissa positioner
försvinner medan andra växer. Den nya mätningen visar i stället hög
positionsvis överlappning mellan två rapportdatum, även med de redovisade
dataluckorna. Det tillför information om ägandet efter indexändringen.
Det är inte en exakt uppdelning av F35:s tidigare nettoförändring: urval,
fondsupport och enhet skiljer sig. Det är heller ingen jämförelse med hur
stor överlappningen normalt är i aktier som inte tillförts indexet.

Det bevisar inte att positionerna hållits oavbrutet: en försäljning och ett
återköp kan ge samma slutposition. Resultatet förklarar inte varför priset
stiger, identifierar inte köporder och avgör inte om priseffekten består.
Det är en explorativ följdfråga efter kända tidigare resultat. Den nya
formeln och källregeln låstes före just denna beräkning; hela forsknings-
processen var inte blind eller förregistrerad. Den första körningen,
oberoende rekonstruktion och rotens omkörning ger samma huvudresultat.

SHOF: VAD SOM NU ÄR HÄMTAT OCH KONTROLLERAT
Tre nya minutexporter totalt i dagens pilot, varav två i denna fortsättning.
Alla fem fasta aktie-dagar är nu validerade, 1 926 minutrader. Köp-/säljkurser
och visade storlekar överensstämmer med sista fullbokstillståndet. Vid åtta
icke-terminala minutslut finns flera tillstånd med samma tidsstämpel; där
avser matchningen sista filrad. Alla fem terminaltillstånd är entydiga och
högst 3,59 sekunder gamla före 17:25. Detta är pilotstöd, inte ett globalt
löfte om sampling och färskhet. Transaktionsfälten har annan semantik.

En Camurus-leverans hade fler datum än formuläret visade. Originalet har
bevarats, avvikelsen redovisas och den filen används bara i överlappskontroll.
Inga extra dagar används som nya observationer. Minut- och fullboksutdragen
innehåller fortfarande inga rader från 17:25: själva stängningsauktionen
har alltså inte återvunnits. Chrome är lämnat fritt.

KVARVARANDE KONKRET DATAKRAV
Två nya dokumenterade LSEG-frågor om auktionsvolym gav en daterad träff för
Camurus 2023 men inget värde/datum för Bilia 2019. Volym ersätter inte pris.
För den större låsta auktionsstudien behövs verifierade slutliga auktions-
avslut även före 2023, för eventaktier och tre fasta kontroller på två dagar.
LSEG Tick History/DataScope och Nasdaqs separata råarkiv är dokumenterade
produktspår, men sådan faktisk konto-/arkivåtkomst har inte verifierats här.
En konkret databeskrivning finns i auction_sources/READY_SOURCE_REQUEST.txt;
den har inte skickats. Fler stora minututtag beställs inte medan denna
bindande lucka kvarstår. Ingen bred auktionsskattning eller ny FTN-analys
har räknats. De tidigare två auktionsfallen är fortfarande enskilda fall.

LÄSORDNING OCH REPRODUKTION
next_test/REPORT_SV.txt samt outcomes/PRIMARY_RESULT.json: nytt ägarresultat.
next_test/PROPOSED_TEST.txt och DESIGN_LOCK.json: exakt formel och faktisk låstid.
next_test/REPLAY_README.txt: oförändrad estimator med verifierade ompekade sökvägar.
overlap_independent/: separat kod från ursprungsdata, inte producentfunktioner.
ROOT_REPLAY_CHECK.json: rotens omkörning och byte-exakta event-/reviewtabeller.
source_validation/FINAL_SOURCE_NOTE_SV.txt och README_REPLAY.txt: femdagarskällkontroll.
design_audit/REPORT_SV.txt: vad som krävs för en större auktionsstudie.
auction_sources/REPORT_SV.txt: dokumenterade alternativa källor och faktiska försök.
ACQUISITION_LEDGER.json är aktuell; äldre lås/delrapporter bevaras som historik.
Rå licensierade priser/innehav och inloggningsuppgifter publiceras inte.
