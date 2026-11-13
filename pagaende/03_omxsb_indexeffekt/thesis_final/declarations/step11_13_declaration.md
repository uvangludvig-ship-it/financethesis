# Deklaration: steg 11 till 13, flytt av redan körda G&S-test till thesis_final

Skriven 10 november 2026, 21:46 CET, innan något av stegen körts i thesis_final.

## Vad det gäller

Inga nya test. Stegen flyttar test som kördes 30 oktober till 2 november och som hittills legat utanför thesis_final, eftersom de kräver hela kurspanelen. Metoden ändras inte.

| Steg | Test | G&S | Ursprung |
|---|---|---|---|
| 11 | Värdeviktad noterad spread per år för OMXSB-bolagen, och tilläggens CAR mot årets spread | Figur 9 | `code/build/mechanisms_2007.py`, E2 (30 okt) |
| 11 | Andel av omsättningen ED±22 som handlas ED−1 och ED | Avsnitt 2.4.3 | samma fil, E5a |
| 11 | Tilläggens rang bland icke-medlemmar, efter omsättning och börsvärde | Figur 8 | samma fil, E4c |
| 12 | Nyemissioner: förändring i log antal aktier [AD−5, ED+60], tillägg mot nästan tillagda | Avsnitt 2.4.3 | `runda11.py`, del F (2 nov) |
| 12 | OMXS30: CAR [AD−1, ED+1] vid ändringar i OMXS30, jämfört med OMXSB | Tabell 8 | `runda10.py`, T28 (2 nov) |
| 13 | Kontrollerna i tabell 2 räknade ur kurserna, även för de 9 borttag som saknar dem | Tabell 2 | `runda11.py` (2 nov) |

## Regler

1. **Samma siffror.** Varje steg jämför sig med den gamla körningen på det gamla urvalet (filerna i `data/comparison/`). Avviker något skrivs det ut. Ingenting justeras för att stämma.
2. **Urval.** Dagens urvalsregel (10 borttag ute, `sample_rule_declaration.md`) gäller där händelserna är borttag ur OMXSB. Tillägg påverkas inte. Där regeln ändrar en siffra visas både nytt och gammalt urval.
3. **Inferens.** Medelvärden och kontraster får samma inferens som tabell 1 (klustrat per översyn, restriktiv wild cluster bootstrap, 9 999 dragningar). Punktskattningarna ska vara desamma som i ursprunget. p-värden kan skilja i sista decimalen eftersom dragningarna är andra.
4. **Steg 13.** Kontrollerna för de händelser som redan har dem ska bli desamma som i `omxsb_changes_corrected_2007_2026.csv`. De 9 borttagen får kontroller med oförändrade definitioner. Tabell 2 för borttag med kontroller får då fler händelser. Både den gamla raden (utan de 9) och den nya redovisas, oavsett utfall.
5. **Allt redovisas.** Ingen rad väljs bort efter utfall. OMXS30 hade för lite styrka 2 november (MDE 3,66 mot gränsen 3) och redovisas därför bara som medelvärden med intervall, som då.

## Tillägg 10 november 2026, 21:55 CET

Steg 13 heter `07_controls_from_prices.py` i koden och körs före steg 09. På Alexanders besked kl. 21:50 (inga nya resultat, bara koden) kopplas det inte in i tabell 2: steg 10 läser kontrollerna ur filen från runda 11, som förut. Punkt 4 ovan gäller därför bara första meningen: kontrollerna ska bli desamma som i runda 11. Ingen tabell ändras av steg 07, 11 eller 12.
