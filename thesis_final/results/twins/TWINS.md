# Steg 16: tvillingar

Port av `twin_prices.py`, `twin_core.py`, `twin_run.py` och `ab_revision.py`, samma frön och ordning.

## Jämförelse med körningen 1–2 november

Alla jämförda siffror är identiska.

## Spread indexslag minus systerslag (procent, eget tecken), placeboinferens

| Fönster | N | Bolag | Medel | p | Medel per bolag | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| primär [AD-1,ED+1] | 39 | 13 | 0.33 | 0.4074 | 0.68 | 0.3222 |  |
| medprimär återgång [ED,ED+20] | 39 | 13 | −0.47 | 0.3050 | −1.17 | 0.1406 |  |
| sek [AD-1,AD+1] | 39 | 13 | 0.70 | 0.0292 | 0.85 | 0.0844 | 0.0876 |
| sek [AD+2,ED-2] | 39 | 13 | 0.07 | 0.8020 | 0.50 | 0.3744 | 0.8020 |
| sek [ED-1,ED+1] | 39 | 13 | −0.44 | 0.1742 | −0.67 | 0.1648 | 0.3484 |
| placebo [AD-60,AD-21] | 39 | 13 | −0.01 | 0.9340 | 0.30 | 0.8366 |  |
| placebo [AD-20,AD-2] | 39 | 13 | −0.27 | 0.5470 | −0.46 | 0.5000 |  |

## A/B-revisionen, primärt fönster [AD−1, ED+1]

| Urval | N | Bolag | Skattning | 95 % intervall | p | Medel per bolag |
|---|---|---|---|---|---|---|
| alla rensade | 39 | 13 | 0.33 | −0.47 till 1.16 | 0.3840 | 0.68 |
| tillägg | 19 | 10 | −0.34 | −1.61 till 1.05 | 0.4848 | −0.30 |
| borttag | 20 | 11 | 0.97 | 0.00 till 2.03 | 0.0490 | 1.31 |
| utan källbyte (bara panelens totalavkastning) | 29 | 9 | 0.04 | −0.59 till 0.65 | 0.9322 | 0.04 |

Status per händelse i revisionen: ok 39.
