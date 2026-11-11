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
