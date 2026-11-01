# A/B-revision, deklarerad 2026-11-01 21:42 CET, innan rensat tvillingtest körs

**Redan kända resultat:**
- Primärt tvillingtest, 39 händelser i 13 bolag, [AD−1, ED+1], indexslag minus systerslag, signerat: +0,33 (−0,53 till 1,19), p 0,41. Per bolag +0,68 (p 0,32).
- Båda slagen mot marknaden: indexslaget +3,18 %, systerslaget +2,85 %.
- Kända datafel (genomgång 2026-11-01 kväll): SCA 2017-06-12 (+27,5 % i kvoten, går inte tillbaka); Husqvarna 2014-10-15/16 (±28 %, går tillbaka); NCC 2008-04-09 (−9,8 % i totalavkastning, −0,2 % i pris); hopp över 8 % i fönstret för Transcom 2009H1 och Sagax 2015H1; systerslag som studsar ofta (Bonava, Ratos, Sweco, Transcom, IFS).

**Regler (gäller både händelsefönster och placebofönster):**
- R1, samma källa: kommer serierna från olika källor (systerslag hämtat separat från LSEG: NCC A, Sweco A, Bonava A, Ratos A) används pris för båda. Annars totalavkastning från panelen för båda.
- R2, topp som går tillbaka: en dag d där kvoten mellan slagen ändras mer än 8 % och dag d+1 tar tillbaka minst 75 % av ändringen. Ett fönster utesluts om dess basdag (start−1) eller slutdag är en sådan dag.
- R3, ojusterad bolagshändelse: en dag där kvoten ändras mer än 15 % och inte går tillbaka (mindre än 25 % återgång dag d+1). Ett fönster som innehåller en sådan dag utesluts.
- R4, stillastående kurser: om systerslagets kurs är oförändrad på mer än 50 % av handelsdagarna i [AD−60, ED+20] utesluts händelsen.
- Mekaniska uteslutningar och bolagshändelser som tidigare (39 händelser är utgångsläget).

**Redovisas:** antal händelser och bolag som faller bort per regel, skattning med 95 % intervall (från placebofördelningen), p, per bolag, och båda slagen mot marknaden. Ett intervall som innehåller 0 betyder "ingen indexslagsspecifik skillnad påvisad", inte att köptryck är uteslutet.
