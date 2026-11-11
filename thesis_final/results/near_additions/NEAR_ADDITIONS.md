# Steg 14: tillägg och borttag mot nästan tillagda (T5v)

Flyttat från `runda2.py` (T5v), metoden oförändrad. Före = beskedet före 2017.

## Jämförelse med runda 2 (alla borttag)

Alla jämförda siffror är desamma (skattning, antal, översyner och analytiskt intervall).

## Resultat: koefficienten för händelse (procentenheter CAR [AD−1, ED+1])

| Typ | Urval | Period | Variant | Skattning | 95 % intervall | p | N | Händelser | Nästan | Översyner |
|---|---|---|---|---|---|---|---|---|---|---|
| addition | alla | före | CAR [AD-1,ED+1] mot nästan | 3.90** | 0.10 till 8.07 | 0.046 | 865 | 78 | 787 | 18 |
| addition | alla | före | känslighet: bara huvudlistan (XSTO) bland nästan | 3.88** | 0.08 till 7.97 | 0.046 | 592 | 78 | 514 | 18 |
| addition | alla | efter | CAR [AD-1,ED+1] mot nästan | 1.53** | 0.36 till 2.68 | 0.015 | 1768 | 159 | 1609 | 19 |
| addition | alla | efter | känslighet: bara huvudlistan (XSTO) bland nästan | 1.39** | 0.12 till 2.60 | 0.036 | 1538 | 159 | 1379 | 19 |
| deletion | utan de 10 (G&S regel) | före | CAR [AD-1,ED+1] mot nästan | −3.24 | −9.27 till 1.17 | 0.210 | 483 | 68 | 415 | 17 |
| deletion | utan de 10 (G&S regel) | före | känslighet: bara huvudlistan (XSTO) bland nästan | −3.69 | −9.65 till 1.17 | 0.184 | 340 | 68 | 272 | 17 |
| deletion | utan de 10 (G&S regel) | efter | CAR [AD-1,ED+1] mot nästan | −1.40* | −2.75 till 0.03 | 0.053 | 963 | 130 | 833 | 19 |
| deletion | utan de 10 (G&S regel) | efter | känslighet: bara huvudlistan (XSTO) bland nästan | −1.38* | −2.83 till 0.21 | 0.078 | 868 | 130 | 738 | 19 |
| deletion | alla | före | CAR [AD-1,ED+1] mot nästan | −3.65 | −9.32 till 0.82 | 0.141 | 489 | 74 | 415 | 17 |
| deletion | alla | före | känslighet: bara huvudlistan (XSTO) bland nästan | −3.83 | −9.57 till 0.91 | 0.140 | 346 | 74 | 272 | 17 |
| deletion | alla | efter | CAR [AD-1,ED+1] mot nästan | −1.42* | −2.79 till 0.02 | 0.053 | 965 | 132 | 833 | 19 |
| deletion | alla | efter | känslighet: bara huvudlistan (XSTO) bland nästan | −1.39* | −2.85 till 0.19 | 0.079 | 870 | 132 | 738 | 19 |
