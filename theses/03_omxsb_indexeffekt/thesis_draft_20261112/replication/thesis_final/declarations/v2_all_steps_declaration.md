# Deklaration: output v2, alla huvudresultat utan händelserna med egen bolagsnyhet

Skriven 2026-11-09 21:16 CET, innan körningen. Bygger på `news_screen_declaration.md`, där bara testen i tabell 1 var deklarerade.

Vad: de händelser som har `contaminated = ja` i `data/events/news_screen_extreme_events.csv` tas bort ur de tre händelsefilerna i `data/events/`, och steg 01 till 06 körs om utan ändring i koden. Fondinnehavens beställningslista lämnas orörd. Resultaten skrivs till `output.v2/`, och `output.v2/check.txt` visar före mot efter (värde = efter, väntat = före).

Läsning, bestämd nu: beskrivande. Huvudtabellerna (`results/`) ändras inte. Bara tabell 1-testen var deklarerade i förväg; resten redovisas som utforskande. Ändras en slutsats (tecken, eller stjärnnivå på ett test som bär en slutsats) skrivs det ut.
