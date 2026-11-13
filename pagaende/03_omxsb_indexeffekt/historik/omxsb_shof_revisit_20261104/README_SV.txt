Aktuell slutstatus: se ../omxsb_source_and_overlap_20261104/README_SV.txt.
Alla fem fasta dagar är nu verifierade; nedanstående text är den bevarade
delsnapshoten från 10:42 UTC med endast Bilia levererad.

SHoF: källgranskning och första minutpilot, 4 november 2026
Teknisk arbetsrapport. Ingen uppsatstext eller ny ekonomisk skattning.

Nytt verifierat resultat
Ett nytt minututtag för Bilia A, 2019-05-31, är nedladdat och bevarat byte-exakt.
Det innehåller 432 minuter. I samtliga återges fullbokens sista köp-/säljkurser,
visade storlekar på två nivåer, handelsstatus och identitet exakt. Ingen
icke-tom minut saknas och inga tomma minuter fylls ut i detta pilotpar.
Den tidigare specificerade kontrollen efter 09:01 ger 424 av 424 träffar.

Vad det löser och inte löser
Det stöder att minututtaget kan ge samma kursläge före auktionen som den
betydligt större fullfilen. För just pilotdagen är den sista giltiga kursen
från 17:24:58.455341783. Minutfilen etiketterar den 17:24:00; den exakta
uppdateringstiden måste därför styrkas genom fullboken. Detta är ännu ingen
verifierad regel för hela historiken. Transaktionsfälten följer inte samma
sista-rad-regel och får inte behandlas som enskilda avslut.

Minutfilen har fortfarande inga rader från 17:25. Den ger alltså inte själva
slutauktionen. Ingen ny auktionspremie eller avkastning har räknats.

Återstående fasta källkontroll
Camurus och AFRY på 23 och 30 november 2023 ingår i samma låsta femdagarsprov.
Ett gemensamt minututtag för 23–30 november har begärts via formuläret, med
en omaktivering när inget kvitto syntes. Ingen leverans eller mottagning har
ännu bekräftats. Det betyder inte att data saknas. Övriga dagar i intervallet
ska ignoreras om filen levereras. De fyra fasta jämförelserna är fortsatt
öppna. Inga extra bolag/dagar eller alternativa ekonomiska fönster har valts.
Chrome har lämnats fritt så användaren kan arbeta i Word; lokala kontroller
kräver ingen webbläsarstyrning. Jobbstatus skiljer bekräftade leveranser från
osäkra knappaktiveringar: ACQUISITION_LEDGER.json och ACCESS_STATUS.json.

Vad den tidigare källgranskningen redan visade
- Fem fullständiga orderböcker slutar 17:24:56–17:24:59, inga rader från 17:25.
- Transactions-uttaget är samma Bilia-avslutsrader som redan finns i fullboken.
- NMQ-uttaget är dagsmått, trots att vissa variabelnamn nämner minuter.
- Buyer/seller saknas på alla rader i de fyra 2023-fullböckerna.
- SHoF:s äldre manual beskriver separata Trade Ticker och Full Day Timeserie.
  Dessa produkters aktuella exporttillgång är fortfarande obekräftad.
  Dagens publika meny verifierar bara reconstructed book och NMQ.
Detta bevisar inte att SHoF:s råarkiv saknar auktioner. En konkret teknisk
förfrågan finns i documentation/DATA_REQUEST_NOT_SENT.txt men har inte skickats.

Åtkomsthistorik
Startsidan meddelade flytt, men officiell navigering ledde tillbaka till samma
exportadress. Native Chrome följde först fel fönster; användaren klargjorde
att två fönster var öppna. En utgången SHoF-session förnyades därefter via HHS.
Bilia kunde då sökas och hämtas. Det tidigare åtkomstproblemet får inte tolkas
som frånvaro av forskningsdata. Ursprungliga statusuppgifter är bevarade i
ACCESS_STATUS.json med denna korrigering av orsakstolkningen.

Underlag
minute_validation/: minutpilotens kod, metadata och källjämförelser.
raw_audit/: kontroll av de sju tidigare bevarade originalen.
documentation/: produkt- och protokollgranskning.
ACQUISITION_LOCK.txt: i förväg låst källurval och högst åtta nya jobb.
Licensed råfiler ligger endast i den git-ignorerade datamappen.
De tidigare ekonomiska pilotresultaten och breda stoppbesluten är oförändrade.
Ingen FTN-analys utförd.
