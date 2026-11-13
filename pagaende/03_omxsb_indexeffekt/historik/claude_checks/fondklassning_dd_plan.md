# Kartläggning av OMXSB-följande fonder (fondklassning, DD)

Skriven 2026-11-04 16:45:43 CET (tid från `date`). Datagenomgång, inget hypotestest. Inga resultatskript ändras.

## Varför
Granskningen 4 nov (TRACKER_AUDIT_2026-11-04) visar att runda 9:s namnregel missar fonder som följde OMXSB (Länsförsäkringar Sverige Index till 2022-05, Handelsbanken Sverige OMXSB Index till 2019-10, Öhman Etisk Index till 2022-11, Danske Invest Sverige Beta) och tar med fonder som inte gör det (Access Edge, Storebrand, Nordea Inst. före 2022), samt att XACT räknas till 2018-12 i stället för 2018-10-09. Målet är en enda daterad mandatfil som alla skript läser.

## Vad som görs, i ordning
1. **FI, alla 886 fonder, 31 kvartal.** Varje fond-kvartal med OMXSB/Benchmark/SBX/OMXSB ESG/Custom OMXSB i jämförelseindex; aktiv risk; innehavslikhet från `indexfond_innehav.csv`. Lista alla fonder som någon gång haft OMXSB-familjen som index.
2. **FI, handelsmönster per fond och år.** För varje fond och år: andel tillägg (borttag) där fonden gick från 0 till >0 (>0 till 0) mellan kvartalet före AD och kvartalet efter ED, bland händelser där fonden rapporterar båda kvartalen. Alla fonder, inte bara kandidaterna. Flagga varje fond med träff ≥ 0,5 något år med minst 4 händelser.
3. **Lipper, alla 10 465 fonder, 2007–2026.** Samma träffmått per fond och år på de 525 händelserna. Flagga samma sätt. Det fångar utländska följare och svenska före 2019.
4. **Sammanställning.** Union av 1–3 och granskningens tabell 2b. Per fond: perioder, skikt (B rent OMXSB; V ESG/custom/indexnära variant; C blandfond med OMXSB-del; X ej följare), status (primärkälla finns / bara FI-benchmark / bara handel / utesluten med skäl).
5. **Utdata:** `data/input/omxsb/tracker_mandates_kandidat.csv` och `fondklassning_dd_rapport.md`. Ludde och Alexander belägger raderna utan primärkälla innan filen döps om till `tracker_mandates.csv` och skripten byggs om.

## Regler
- Inget resultat räknas om i denna körning. Bara klassning.
- En fond som handlar som följare men saknar dokument flaggas, tas inte tyst med eller bort.
- Trösklar (0,5; 4 händelser) är sökhjälp, inte urvalsregel; urvalet avgörs av mandat med datum.
