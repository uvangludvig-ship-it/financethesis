# Deklaration: steg 13 till 16, flytt av redan deklarerade och körda test till thesis_final

Skriven 11 november 2026, 13:36 CET, innan något av stegen körts i thesis_final.

## Vad det gäller

Inga nya test. Stegen flyttar in test som redan är deklarerade och körda, så att de körs av `run_all.py` och kontrolleras av `08_check_numbers.py`. Metoden ändras inte. Inferensen görs med `lin()` från steg 01 (klustrat per översyn, restriktiv wild cluster bootstrap, intervall genom testinversion), utom där testet hade en egen inferens som ska återskapas exakt (tvillingarna).

| Steg | Test | Ursprung |
|---|---|---|
| 13 | Extremvärden: tabell 1 med CAR winsoriserad vid 1:a och 99:e percentilen (gränserna från alla 481 händelser med CAR), utan händelser med \|CAR\| > 20 %, och utan Sivers; median per period; M för tillägg 2017–21, 2022–26 och 2017–26 med och utan de 12 händelserna med egen bolagsnyhet | Robusthetsdiskussionen 11 nov och nyhetsgenomgången (`news_screen_declaration.md`) |
| 14 | T5v: tillägg och borttag mot nästan tillagda och nästan borttagna, CAR [AD−1, ED+1] på händelse, uppgång och log börsvärde med fasta effekter per översyn; känslighet med bara huvudlistan (XSTO) bland de nästan tillagda | `code/claude_checks/runda2.py`, `runda2_deklaration.md` |
| 15 | Återgång efter ändringen: CAR [ED, ED+10], CAR [ED, ED+20] och uppgången [AD, ED−1], alla och per period; återgångsandelen över 20 dagar | `code/claude_checks/del1.py` |
| 16 | Tvillingar (aktieslag i samma bolag där bara det ena är med i OMXSB): primärt fönster, återgång, sekundära fönster och placebo, med samma placebofördelning och samma frön (11 och 20261101); A/B-revisionen | `code/claude_checks/twin_*.py`, `ab_revision.py`, `ab_deklaration.md`, `twin_excl_beslut.md` |

## Urval

- Urvalsregeln från 10 november (`sample_rule_declaration.md`) gäller borttag: de 10 borttag som G&S regel utesluter tas bort. Där testet kördes på alla borttag redovisas båda urvalen (steg 14 och 15), så att den gamla siffran går att återskapa.
- Tillägg påverkas inte av regeln.
- Steg 13: winsoriseringsgränserna räknas på alla 481 händelser med CAR (även de 10 borttagen), och tillämpas sedan på urvalet i tabell 1.
- Steg 16 har ett eget urval (tvillingparen) som inte ändras.

## Vad som ska stämma

- Samma siffror som förut på det gamla urvalet. Jämförelsen görs mot filer i `data/comparison/` (de gamla körningarnas resultat), och kontrollsiffrorna läggs in i `08_check_numbers.py`.
- Stämmer en kontrollsiffra inte stoppas arbetet och skillnaden skrivs ut. Inget justeras för att få siffran att stämma.
- p-värden och intervall kan skilja sig från de gamla körningarna där inferensen byts till `lin()` (andra dragningar, testinversion i stället för analytiskt intervall). Punktskattningar och antal ska vara desamma.

## Läsning, bestämd nu

- Huvudtabellen (tabell 1 och 2) ändras inte. Extremvärdena redovisas som robusthet i en egen bilagetabell (A5).
- Nästan tillagda, återgången och tvillingarna redovisas i egna tabeller efter tabell 10.
