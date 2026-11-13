# Deklaration: splitjustering av aktieantalet i nyemissionstestet (steg 12 del A, tabell 8)

Skriven 11 november 2026, 20:06:48 CET, innan koden ändrades.

## Felet

Hittat 11 november 2026. Nyemissionstestet mäter förändringen i log antal aktier i bolaget (alla noterade aktieslag) från AD−5 till
ED+60. Aktieantalet i panelen är inte justerat för splittar, så en split eller sammanläggning räknas som en emission. 71 av 2 586
rader har |dlog| > 30.

## Utfallet är känt

En utforskande körning är redan gjord, så utfallet är känt innan rättelsen: skillnaden tillägg minus nästan tillagda är 0,50
(p 0,69) utan justering och 0,99 (p 0,042) med full justering. Rättelsen nedan är bestämd utifrån felet, inte utifrån utfallet,
men läsaren ska veta att utfallet var känt.

## Rättelsen

- faktor(c, i) = börsvärde / (summa aktier i bolagets noterade slag × justerad stängningskurs), som i runda11.py: kvoten mellan
  ojusterat och justerat pris.
- a = iA − 5, b = iE + 60. dlog_just = dlog + 100 · ln(faktor(b) / faktor(a)) när |ln(faktor(b) / faktor(a))| > ln(1,4);
  annars dlog_just = dlog. Gränsen 1,4 är samma som för splittar i runda11.py.
- Huvudraden: samma regression som förut (tilläggsdummy med fasta effekter per översyn, lin(): klustrat per översyn, restriktiv
  wild cluster bootstrap) på dlog_just. Raden utan justering behålls som jämförelse, märkt "utan splitjustering".
- Nya rader med samma inferens: andel med ökning över 1 % och över 5 % (0/1 × 100, alltså procentenheter).
- De 20 största |dlog_just| skrivs ut med bolag och översyn i ISSUANCE_OMXS30.md, för kontroll för hand mot pressmeddelanden.
- Inga andra test ändras. Del B (OMXS30) är oförändrad.

## Tillägg 11 november 2026, 20:22:18 CET (efter körningen med gränsen 1,4, innan den här regeln kördes)

Utfallet med gränsen 1,4 är känt: 1,01 (p 0,063). Genomgången rad för rad av de 61 justerade raderna visade två fel i regeln,
oberoende av utfallet:

1. Faktorn rör sig utan att aktieantalet ändras (Bergman & Beving 2017H1, Acando 2014H1, Sagax/SFAST 2021H1, Xano 2014H1,
   Volati 2026H1): justeringen skapar en ändring på 37–73 procent som inte finns.
2. Vid företrädesemissioner med rabatt justeras även det historiska priset, så faktorn tar bort en del av en verklig emission
   (t.ex. Intrum 2026H1, Kahl 2011H2, SOBI 2009H2, Coala 2008H2, Hansa/HLDX 2011H1).

Vid en split ändras aktieantalet och faktorn lika mycket (kvoten 2, 3, 4, 10 ...), så dlog + 100·ln(faktor(b)/faktor(a)) ≈ 0.

Ny huvudregel: en rad räknas som split, och justeras, bara när |ln(faktor(b)/faktor(a))| > ln(1,4) och faktorn förklarar
aktieändringen inom 10 procent, |dlog + 100·ln(faktor(b)/faktor(a))| ≤ 100·ln(1,1). Annars dlog_just = dlog (ingen justering).
En split och en emission i samma fönster räknas då utan justering; sådana rader listas för kontroll för hand.

Regeln med bara gränsen 1,4 redovisas som känslighetsrad ("gräns 1,4 utan matchning") och den råa raden som förut. Alla tre rader
redovisas oavsett utfall.
