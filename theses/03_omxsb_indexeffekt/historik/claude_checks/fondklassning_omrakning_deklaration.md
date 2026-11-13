# Omräkning med daterad fondklassning (runda 13)

Skriven 2026-11-04 17:46:37 CET (tid från `date`). Committas innan omräkningen körs på den slutliga listan.

## Vad som ändras
En enda fil, `data/input/omxsb/tracker_mandates.csv` (nu `_kandidat`), ersätter namnreglerna i `runda9.py` (`grupp()`), fondlistan i `shof_aum.py` och de 14 fonderna i Ludvigs `index_funds.csv`. Filen har en rad per fond och mandatperiod: fond, FI-nummer, LSEG-namn (regex), index, skikt, start, slut, källa, status.

Skikt: **B** rena OMXSB-följare; **V** ESG-, custom- och indexnära varianter av OMXSB; **C** blandfonder med en passiv OMXSB-del; **X** fonder med OMXSB som benchmark utan att följa det (räknas som övriga passiva om indexnära, annars aktiva); OMXS30 och småbolagsindex som förut.

## Regler
1. En fond räknas till ett skikt vid en händelse bara om mandatet gäller vid **både** rapporten före AD och rapporten efter ED. Byter fonden mandat däremellan utesluts den från händelsen. Inga falska flöden av mandatbyten.
2. Rapportregeln från runda 9 behålls: rapport inom 120 dagar före AD och 45 dagar efter ED; saknat innehav i en sådan rapport = 0.
3. D saknas (inte 0) när ingen fond i skiktet rapporterar runt händelsen.
4. Tre mått: D_B (bara B), D_V (B + V), D_C (B + V + C). **D_V är huvudmåttet** för jämförelsen med G&S, som räknar indexfonder och ETF:er. D_C är allt OMXSB-länkat passivt kapital. D_B är känslighet.
5. Fonder utan rad i filen klassas som i runda 9 (OMXS30, småbolagsindex, övriga passiva, ej passiv), men aldrig som OMXSB-följare.
6. Rader med status "att belägga" ingår bara om källsökningen ger VERIFIERAD eller om handelsmönstret ensamt räcker för att klassa fonden som icke-följare. En följare utan källa redovisas som känslighet, inte i huvudmåttet.

## Vad som räknas om
- Tabell 5 (M per period, totalt och långt fönster), tabell 6 (M med kontroller, H11a och H11b), tabell 7 (vem handlar: B, V, C, övriga passiva, aktiva, alla fonder), figur 1 (D per år och ägarandel), T24–T26, steg 0-jämförelsen mot FI (`nettokop_v2_events.csv`).
- SHoF-serien: fondförmögenhet per skikt med samma daterade medlemskap; blandfonder vägda med OMXSB-andelen i jämförelseindexet.
- Inferens, fönster, urval och CAR är oförändrade från runda 11 och rättelserna 3 nov. Händelsefilen `handelser_rattade.csv` återanvänds; bara kolumnerna för fondgrupper byts.

## Redan känt
Granskningen 4 nov (TRACKER_AUDIT) har redan publicerat utfall under B, V och C: D_V 2017–21 0,98, 2022–26 0,79; M_V 2017–21 3,4, 2022–26 2,9; ägarandel V 2025 1,14 %. Omräkningen är därför inte blind. Den är en replikering av granskningen med en verifierad fil och de fyra nya kandidaterna.

## Tolkning, bestämd i förväg
- Nivån på D, M och ägarandel redovisas med alla tre skikten. Skiljer sig B och C med mer än en faktor två, skrivs det ut.
- "M har fallit sedan 2017" påstås bara om intervallen skiljer perioderna åt under V. Granskningen visar att de inte gör det.
- Det som står sig oavsett skikt redovisas som huvudresultat: alla fonder köper cirka 1,25 %, aktiva fonder rör sig inte, inget samband CAR–D per händelse, ägandet från nära noll till omkring en procent.
