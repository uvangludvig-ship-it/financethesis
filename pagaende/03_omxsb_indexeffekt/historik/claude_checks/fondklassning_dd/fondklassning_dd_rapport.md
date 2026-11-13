# Kartläggning av OMXSB-följande fonder: rapport

Skriven 2026-11-04 16:53:21 CET (tid från `date`). Plan: `fondklassning_dd_plan.md` (16:45:43). Datagenomgång, inget hypotestest. Inga resultatskript ändrade, inga resultat omräknade.

## 1. Vad som gjordes

Tre sökningar, oberoende av fondnamn:

1. **FI, jämförelseindex.** Alla 886 fonder i FI:s kvartalsdata, 31 kvartal 2018Q4 till 2026Q2. Varje fond som någon gång angett OMXSB, OMXSB Cap, SBX, OMXSB ESG eller Custom OMXSB som jämförelseindex: 100 fonder (`steg1_fi_jmf_kandidater.csv`). De flesta är aktiva fonder som bara mäter sig mot indexet.
2. **FI, handelsmönster.** För varje fond och år: andelen tillägg där fonden gick från noll till ägare mellan kvartalet före beskedet och kvartalet efter ändringen, bland händelser där fonden rapporterar båda kvartalen. 251 händelser med FI-kvartal. Måttet är ovillkorat: alla rapporterande fonder ingår, oavsett om de ägde aktien (`steg2_fi_traff_per_fond_ar.csv`).
3. **Lipper, handelsmönster 2007 till 2026.** Samma mått för alla 10 465 fonder i LSEG-uttaget på de 525 händelserna, med runda 9:s rapportregel (rapport inom 120 dagar före beskedet och 45 dagar efter ändringen). Måttet är villkorat: en fond finns bara med för händelser där den ägde aktien i någon av rapporterna. Lipper-träffarna är därför högre än FI-träffarna för samma fond (`steg3_lseg_tillagg_traff_matris.csv`).

Resultaten slogs ihop med granskningens tabell 2b (`TRACKER_AUDIT_2026-11-04`) till `tracker_mandates_kandidat.csv`.

## 2. Alla fonder som någon gång följt OMXSB, med period, skikt och status

Skikt: B = kopierar OMXSB eller OMXSB Cap (ofta med exkluderingar). V = ESG-, custom- eller indexnära variant av OMXSB. C = blandfond med passiv OMXSB-del. X = har OMXSB som jämförelseindex men följer det inte.

| Fond | Index | Skikt | Start | Slut | Status | Källtyp |
|---|---|---|---|---|---|---|
| XACT OMXSB (nu XACT Sverige) | OMXSB GI | B | 2003-06-02 | 2018-10-09 | verifierad | primär |
| Handelsbanken Sverige OMXSB Index (nu Sverige 100 Index Criteria) | OMXSBGI | B | 2011-08-30 | 2019-10-06 | verifierad | primär |
| Länsförsäkringar Sverige Indexnära / Sverige Index | OMXSB Cap | B | 2008-11-17 | 2022-05-11 | verifierad | primär |
| Länsförsäkringar Sverige Index | Morningstar Sweden PAB Select | X | 2022-05-12 | 2025-06-15 | verifierad | primär |
| Länsförsäkringar Sverige Index | Custom OMX Stockholm Benchmark | V | 2025-06-16 | pågår | verifierad | primär |
| Nordnet Superfonden Sverige / Indexfond Sverige | OMXSB GI (SBX) | B | 2009-03-10 | 2022-05-31 | verifierad | primär |
| Nordnet Indexfond Sverige ESG / Sverige Index | OMXSB ESG Responsible GI | V | 2022-06-01 | pågår | verifierad | primär |
| Nordea Indexfond Sverige / Sverige Passiv | OMXSB Cap | B | 2008-09-01 | pågår | verifierad för FI-perioden; namnbytesdatum saknas | primär (nuvarande) + FI |
| Swedbank Robur Access Sverige | OMXSB Cap GI | B | 2015-09-10 | pågår | verifierad | primär |
| iShares OMX Stockholm Capped UCITS ETF | OMXSB Cap | B | 2016-12-14 | pågår | verifierad | primär |
| Danske Invest SICAV Sverige Beta | OMXSB Cap Net | B | 2017-11-13 | pågår | att belägga: index och fondens start | primär (startdatum andelsklass) |
| Danske Invest Index Sweden Restricted | okänt, troligen OMXSB-variant | V? | 2020 | pågår | att belägga: index, start, fondtyp | handel |
| Öhman Etisk Index Sverige (nu Lannebo Marknad Sverige Bred) | OMX SBXCAP GI | V | 2011 | 2022-11-29 | verifierad; startår att belägga | primär |
| Öhman Marknad Sverige (nu Lannebo Marknad Sverige) | OMX SBXCAP GI | V | 2017-06-20 | pågår | verifierad | primär |
| Nordea Institutionella Aktiefonden Sverige | OMXSB Cap ESG | V | 2022-04-01 | pågår | att belägga: besked om passiv förvaltning | FI + handel |
| SEB Sverige Indexfond (f.d. Swedish Ethical Beta / SEB Hållbarhetsfond Sverige Index) | okänt 2012–2018, troligen OMXSB Cap; SIX Sweden Sustainability från senast 2019Q4 | B? | 2012 | 2018 | att belägga: fondbestämmelser 2012–2018 | handel |
| SEB Sverige Indexnära | okänt 2011–2012; SIX från senast 2019 | B? | 2011 | 2012 | att belägga | handel |
| Skandia Sverige Exponering | okänt 2013–2017; SIX Portfolio från senast 2018Q4 | B? | 2013 | 2017 | att belägga: fondbestämmelser 2013–2018 | handel |
| Swedbank Robur Access Mix (f.d. Mix Indexfond Sverige) | 50 % OMXSB Cap GI + 50 % OMRX | C | ? | pågår | verifierad; startdatum för indexdelen saknas | primär |
| Nordea Generationsfond 50/60/70/80/90-tal, Senior | OMXSB Cap ESG-del 3–14 % | C | 2021-10-01 | pågår | att belägga: besked om passiv svensk del | FI + handel |
| Nordea Stiftelse- och Donationsmedelsfond | OMXSB ESG Responsible Capped 33 % | C | 2022-03-01 | pågår | att belägga: passiv förvaltning | primär (jmf) |
| KPA Etisk Blandfond 2 / KPA Blandfond | OMXSB Cap Gross 33 % | C | 2023-03-14 | pågår | verifierad | primär |
| Länsförsäkringar Sparmål 2025–2065 (6) | Custom OMXSB-del (svensk aktiedel) | C | 2025-06-16 | pågår | att belägga: dokumentet säger Morningstar, handeln säger OMXSB | FI + handel; motstridigt dokument |
| Swedbank Robur Access Edge Sweden | OMXSB Cap GI (benchmark) | X | 2020-02-25 | pågår | verifierad | primär |
| SPP Aktiefond Sverige / Storebrand Sverige | OMXSB Cap GI (benchmark) | X | ? | pågår | verifierad | primär |
| GodFond Sverige & Världen | 50 % OMXSB Cap (benchmark) | X | ? | pågår | verifierad som ej följare | FI + handel |
| Nordea 2 SICAV BetaPlus Enhanced Swedish Sustainable Equity | okänt (enhanced) | X? | 2022 | pågår | att bedöma | handel |
| Handelsbanken Stiftelsefond | blandfond, SIX SRI Sweden-del | X | ? | pågår | ej följare | FI |
| Avanza Zero / XACT OMXS30 / Aktiespararna Topp Sverige | OMXS30 | OMXS30 | ? | pågår | verifierad | FI |

Källor med länk står i kolumnen `kalla` i csv-filen. 18 rader är verifierade mot primärkälla eller FI:s jämförelseindex. 11 rader behöver beläggas.

## 3. Felen i runda 9:s regel

Regeln i `runda9.py` klassar fonder efter dagens namn i LSEG. Det gav:

- **Saknade följare.** Länsförsäkringar Sverige Index (OMXSB Cap 2008 till maj 2022, 12 till 28 miljarder) låg i "övriga passiva". Handelsbanken Sverige OMXSB Index (OMXSBGI 2011 till oktober 2019) låg i "övriga passiva". Öhman Etisk Index Sverige (OMX SBXCAP till november 2022) räknades som aktiv, eftersom den nu heter Lannebo Marknad Sverige Bred. Danske Invest Sverige Beta räknades som aktiv.
- **Felaktigt medräknade.** Robur Access Edge Sweden (indexnära, aktiv risk 1,1 till 2,0, FI-träff 0,2 till 0,6). Storebrand Sverige från oktober 2025 (indexnära, FI-träff 0,1 till 0,5). Nordea Institutionella Aktiefonden alla år, fast den handlar som följare först från 2022.
- **Fel datum.** XACT räknades till 2018-12-31. Indexbytet var 2018-10-09.

Följd: D för lågt 2012 till 2021, M för högt, och figur 1 byggd på en annan fondgrupp än D.

## 4. Nya kandidater som inte finns i granskningen

Fyra fonder handlar som följare under perioder som ingen tidigare lista täcker. Alla saknar primärkälla och ska beläggas innan de används.

| Fond | Period enligt handeln | Lipper-träff | Behöver |
|---|---|---|---|
| Danske Invest Index Sweden Restricted (DK) | 2020 till 2026 | 0,93 till 1,00 2020 till 2024; 0,42 2025; 0,88 2026 | Fondbestämmelser: vilket index, från när. Finns bara i Lipper |
| SEB Sverige Indexfond (f.d. Swedish Ethical Beta, SEB Hållbarhetsfond Sverige Index) | 2012 till 2018 | 1,00 åren 2012, 2013, 2015, 2016, 2017; 0,00 från 2019 | SEB:s fondbestämmelser eller årsberättelser 2012 till 2018. Från 2019 SIX Sweden Sustainability enligt FI |
| Skandia Sverige Exponering | 2013 till 2017 | 1,00 (2013), 1,00 (2016), 0,94 (2017); 0,38 2018; 0,00 från 2019 | Skandias fondbestämmelser 2013 till 2018. Från 2018Q4 SIX Portfolio enligt FI |
| SEB Sverige Indexnära | 2011 till 2012 | 0,75 (2011, 4 händelser), 1,00 (2012, 12); 0,00 från 2013 | SEB:s fondbestämmelser 2011 till 2013. Liten |

## 5. Kontrollerade och uteslutna

| Fond | Skäl |
|---|---|
| GodFond Sverige & Världen | 50 % OMXSB Cap i jämförelseindex, men FI-träff 0,00 till 0,12. Handlar inte vid översyner. Innehavsregeln (`indexfond_innehav.csv`) klassade den fel i 24 kvartal |
| Nordea Stratega 15, 35, 50, 70; Nordea Avtalspensionsfond Midi | Innehavsregeln klassade dem som OMXSB-fonder vissa kvartal. FI-träff högst 0,23. Blandfonder utan passiv handel |
| SEB Active 20, 30, 55, 80 | Samma: innehavsregeln, FI-träff högst 0,17 |
| Nordea 2 SICAV BetaPlus Enhanced Swedish Sustainable Equity | Lipper-träff 0,11 till 0,67. Enhanced index, indexnära. Liten. Bedöms som X om inget dokument säger annat |
| Handelsbanken Stiftelsefond | Lipper-träff 0,75 (2009, 4 händelser) och 0,86 (2011), sedan 0. Blandfond med SIX SRI Sweden-del enligt FI. Ingen OMXSB-koppling |
| Danske Invest Allocation Horisont Aktie | Fondandelsfond. Träffen 2021 och 2025 speglar underliggande fonder. Räknas inte |
| Robur Access Edge Sweden, Storebrand Sverige | Indexnära, se avsnitt 3 |

## 6. Fullständighet

- **2019 till 2026.** Ingen fond i FI utanför listan har träff över 0,25 något år. Alla 886 fonder är prövade med både jämförelseindex och handel. Listan är så komplett som FI-datan tillåter.
- **2007 till 2018.** Bara Lipper finns. Lipper täcker fonder som rapporterar till Lipper; svenska fonder är 18 procent av raderna. En svensk eller utländsk följare som inte finns i Lipper syns inte. Listan för de åren är en nedre gräns, och D för de åren likaså. Det ska stå i uppsatsen.
- Fyra fonder i listan saknar primärkälla för sitt mandat (avsnitt 4). Tre till saknar dokument för att den svenska delen förvaltas passivt (Nordea Generationsfonder, Donationsmedelsfonden, Institutionella Aktiefonden). Länsförsäkringar Sparmål har ett dokument som säger Morningstar medan handeln säger OMXSB.

## 7. Öppna punkter för Ludvig och Alexander

Rader med status "att belägga" i csv-filen:

1. Danske Invest SICAV Sverige Beta: index och fondens startdatum (inte andelsklassens).
2. Danske Invest Index Sweden Restricted: index, start, fondtyp.
3. SEB Sverige Indexfond 2012 till 2018: fondbestämmelser.
4. SEB Sverige Indexnära 2011 till 2012: fondbestämmelser.
5. Skandia Sverige Exponering 2013 till 2018: fondbestämmelser.
6. Nordea Institutionella Aktiefonden: besked om passiv förvaltning från 2022.
7. Nordea Generationsfonder: besked om passiv svensk del från 2021Q4.
8. Nordea Stiftelse- och Donationsmedelsfond: samma.
9. Länsförsäkringar Sparmål: vilket index den svenska delen följer från juni 2025.
10. Öhman Etisk Index Sverige: startår för OMXSB-mandatet.
11. Nordea Sverige Passiv: datum för namnbytet från Indexfond Sverige. Robur Access Mix: startdatum för indexdelen.

## 8. Nästa steg

1. Ludvig och Alexander belägger raderna ovan och rättar csv-filen.
2. Filen döps om till `data/input/omxsb/tracker_mandates.csv`.
3. `runda9.py`, `runda11.py`, `rattelser_2026-11-03.py`, `shof_aum.py` och `nettokop_v2.py` byggs om så att de läser filen. En fond räknas för en händelse bara om mandatet gäller vid både rapporten före och efter.
4. Tabell 4, 5 och figur 1 räknas om med V som huvudmått, B och C som känslighet, efter deklaration.
5. Inga resultat är omräknade i denna runda.

## Bilaga A. FI-träff per fond och år, tillägg 2019 till 2026 (ovillkorad; antal händelser inom parentes)

| Fond (FI-id) | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| Nordea Sverige Passiv (60293) | 0.50 (10) | 0.76 (25) | 0.53 (17) | 0.62 (29) | 0.46 (13) | 0.76 (17) | 0.82 (17) | 0.82 (11) |
| Nordnet Sverige Index (60320) | 0.60 (10) | 0.76 (25) | 0.59 (17) | 0.59 (29) | 0.54 (13) | 0.76 (17) | 0.82 (17) | 0.55 (11) |
| Swedbank Robur Access Sverige (60824) | 0.50 (10) | 0.64 (25) | 0.35 (17) | 0.45 (29) | 0.31 (13) | 0.47 (17) | 0.59 (17) | 0.36 (11) |
| Länsförsäkringar Sverige Index (60310) | 0.60 (10) | 0.76 (25) | 0.47 (17) | 0.14 (29) | 0.08 (13) | 0.00 (17) | 0.76 (17) | 0.64 (11) |
| Handelsbanken Sverige 100 Index Criteria (60479) | 0.60 (10) | 0.12 (25) | 0.12 (17) | 0.03 (29) | 0.08 (13) | 0.06 (17) | 0.00 (17) | 0.18 (11) |
| Lannebo Marknad Sverige Bred (60029) | 0.30 (10) | 0.40 (25) | 0.24 (17) | 0.38 (29) | 0.15 (13) | 0.12 (17) | 0.00 (17) | 0.09 (11) |
| Lannebo Marknad Sverige (60967) | 0.30 (10) | 0.40 (25) | 0.24 (17) | 0.24 (29) | 0.38 (13) | 0.76 (17) | 0.65 (17) | 0.55 (11) |
| Institutionella Aktiefonden Sverige (51437) | 0.30 (10) | 0.32 (25) | 0.12 (17) | 0.45 (29) | 0.46 (13) | 0.76 (17) | 0.76 (17) | 0.55 (11) |
| Nordea Generationsfond 50-tal (51615) | 0.30 (10) | 0.32 (25) | 0.12 (17) | 0.45 (29) | 0.46 (13) | 0.71 (17) | 0.76 (17) | 0.55 (11) |
| Nordea Generationsfond 60-tal (51617) | 0.30 (10) | 0.32 (25) | 0.12 (17) | 0.45 (29) | 0.46 (13) | 0.71 (17) | 0.76 (17) | 0.55 (11) |
| Nordea Generationsfond 70-tal (51619) | 0.30 (10) | 0.32 (25) | 0.12 (17) | 0.45 (29) | 0.46 (13) | 0.71 (17) | 0.76 (17) | 0.55 (11) |
| Nordea Generationsfond 80-tal (51621) | 0.30 (10) | 0.32 (25) | 0.12 (17) | 0.45 (29) | 0.46 (13) | 0.71 (17) | 0.76 (17) | 0.55 (11) |
| Nordea Generationsfond 90-tal (60718) | 0.30 (10) | 0.32 (25) | 0.12 (17) | 0.45 (29) | 0.46 (13) | 0.71 (17) | 0.76 (17) | 0.55 (11) |
| Nordea Generationsfond Senior (51613) | 0.30 (10) | 0.32 (25) | 0.12 (17) | 0.45 (29) | 0.46 (13) | 0.71 (17) | 0.76 (17) | 0.55 (11) |
| Nordea Stiftelse- och Donationsmedelsfond (51128) | 0.00 (10) | 0.32 (25) | 0.12 (17) | 0.45 (29) | 0.46 (13) | 0.76 (17) | 0.76 (17) | 0.55 (11) |
| Swedbank Robur Access Mix (52163) | 0.50 (10) | 0.76 (25) | 0.35 (17) | 0.55 (29) | 0.31 (13) | 0.59 (17) | 0.71 (17) | 0.27 (11) |
| KPA Blandfond (56020) | 0.00 (10) | 0.00 (25) | 0.00 (17) | 0.00 (29) | 0.23 (13) | 0.41 (17) | 0.29 (17) | 0.45 (11) |
| Länsförsäkringar Sparmål 2025 (56015) | 0.00 (10) | 0.00 (25) | 0.00 (17) | 0.07 (29) | 0.08 (13) | 0.00 (17) | 0.76 (17) | 0.45 (11) |
| Länsförsäkringar Sparmål 2030 (56016) | 0.00 (10) | 0.00 (25) | 0.00 (17) | 0.07 (29) | 0.08 (13) | 0.00 (17) | 0.76 (17) | 0.45 (11) |
| Länsförsäkringar Sparmål 2035 (51639) | 0.00 (10) | 0.00 (25) | 0.00 (17) | 0.07 (29) | 0.08 (13) | 0.00 (17) | 0.76 (17) | 0.45 (11) |
| Länsförsäkringar Sparmål 2040 (51640) | 0.00 (10) | 0.00 (25) | 0.00 (17) | 0.07 (29) | 0.08 (13) | 0.00 (17) | 0.76 (17) | 0.45 (11) |
| Länsförsäkringar Sparmål 2045 (51700) | 0.00 (10) | 0.00 (25) | 0.00 (17) | 0.07 (29) | 0.08 (13) | 0.00 (17) | 0.76 (17) | 0.45 (11) |
| Länsförsäkringar Sparmål 2065 (55624) | . | 0.00 (19) | 0.00 (17) | 0.07 (29) | 0.08 (13) | 0.00 (17) | 0.76 (17) | 0.45 (11) |
| Swedbank Robur Access Edge Sweden (51080) | . | 0.28 (25) | 0.12 (17) | 0.21 (29) | 0.08 (13) | 0.06 (17) | 0.12 (17) | 0.27 (11) |
| Storebrand Sverige (51482) | 0.10 (10) | 0.48 (25) | 0.18 (17) | 0.17 (29) | 0.15 (13) | 0.29 (17) | 0.29 (17) | 0.55 (11) |
| GodFond Sverige & Världen (60330) | 0.00 (10) | 0.00 (25) | 0.06 (17) | 0.03 (29) | 0.00 (13) | 0.24 (17) | 0.12 (17) | 0.09 (11) |
| SEB Sverige Indexfond (60087) | 0.00 (10) | 0.00 (25) | 0.12 (17) | 0.03 (29) | 0.08 (13) | 0.00 (17) | 0.00 (17) | 0.00 (11) |
| SEB Sverige Indexnära (60302) | 0.00 (10) | 0.00 (25) | 0.00 (17) | 0.03 (29) | 0.00 (13) | 0.00 (17) | 0.00 (17) | 0.00 (11) |
| Skandia Sverige Exponering (60638) | 0.00 (10) | 0.00 (25) | 0.00 (17) | 0.03 (29) | 0.00 (13) | 0.06 (17) | 0.00 (17) | 0.00 (11) |

## Bilaga B. Lipper-träff per fond och år, tillägg 2008 till 2026 (villkorad på att fonden ägde aktien i någon rapport; antal händelser inom parentes; celler med färre än 3 händelser utelämnade)

| Fond (LSEG-namn) | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XACT Sverige (UCITS ETF) | . | 0.75 (4) | . | 1.00 (7) | 1.00 (12) | 1.00 (8) | 0.88 (8) | 1.00 (11) | 1.00 (17) | 0.94 (16) | 0.40 (15) | 0.17 (6) | 0.11 (9) | 0.00 (5) | 0.11 (9) | 0.33 (6) | 0.20 (5) | 0.10 (10) | 0.25 (4) |
| Handelsbanken Sverige 100 Index Criteria | . | . | . | 1.00 (4) | . | 1.00 (8) | 0.75 (8) | 1.00 (11) | 0.94 (17) | 0.94 (16) | 0.94 (17) | 0.50 (10) | 0.24 (17) | 0.22 (9) | 0.19 (16) | 0.20 (10) | 0.11 (9) | 0.00 (11) | 0.33 (6) |
| Lansforsakringar Sverige Index | . | . | 1.00 (6) | 1.00 (4) | 1.00 (12) | 1.00 (8) | . | 1.00 (7) | 1.00 (9) | 1.00 (15) | 0.94 (17) | 1.00 (10) | 1.00 (25) | 0.88 (17) | 0.26 (19) | 0.17 (6) | 0.00 (8) | 0.73 (22) | 1.00 (9) |
| Nordnet Sverige Index | . | 1.00 (3) | . | 0.75 (8) | . | . | . | . | 1.00 (9) | 1.00 (15) | 1.00 (16) | 1.00 (10) | 1.00 (25) | 0.89 (19) | 0.91 (11) | . | 1.00 (16) | . | . |
| Nordea Sverige Passiv | . | 1.00 (8) | . | 1.00 (11) | 1.00 (12) | 1.00 (8) | 0.88 (8) | 1.00 (7) | 1.00 (17) | 0.94 (16) | 0.94 (17) | 1.00 (9) | 1.00 (25) | 1.00 (16) | 1.00 (29) | 0.92 (13) | 0.89 (9) | 0.74 (23) | 1.00 (11) |
| Swedbank Robur Access Sverige | . | . | . | . | . | . | . | 1.00 (7) | 0.89 (9) | 1.00 (13) | 0.81 (16) | 0.90 (10) | 0.96 (23) | 0.86 (14) | 0.88 (24) | 0.82 (11) | 0.85 (13) | 0.58 (19) | 0.86 (7) |
| iShares OMX Stockholm Capped UCITS ETF | . | . | . | . | . | . | . | . | . | 1.00 (15) | 0.94 (17) | 1.00 (10) | 1.00 (25) | 0.89 (18) | 0.97 (30) | 0.93 (14) | 0.94 (18) | 0.74 (23) | 1.00 (11) |
| Danske Invest SICAV Sverige Beta | . | . | . | . | . | . | . | . | . | . | 0.93 (15) | 1.00 (9) | . | 0.93 (15) | 0.93 (28) | 0.88 (8) | 1.00 (8) | 0.74 (23) | . |
| Danske Invest Index Sweden Restricted - Accumulating KL | . | . | . | . | . | . | . | . | . | . | . | . | 1.00 (24) | 0.94 (18) | 0.93 (27) | 0.93 (14) | 1.00 (8) | 0.42 (19) | 0.88 (8) |
| Lannebo Marknad Sverige Bred | . | 1.00 (4) | . | 0.89 (9) | . | 1.00 (8) | . | 1.00 (6) | 1.00 (9) | 1.00 (13) | 0.70 (10) | 0.86 (7) | 0.94 (17) | 0.70 (10) | 0.81 (21) | 0.27 (11) | 0.15 (13) | 0.06 (18) | 0.14 (7) |
| Lannebo Marknad Sverige | . | . | . | . | . | . | . | . | . | . | 0.71 (7) | 1.00 (6) | 0.94 (17) | 0.70 (10) | 0.67 (18) | 0.82 (11) | 0.93 (15) | 0.78 (18) | 1.00 (8) |
| Nordea Inst Aktief Sverige icke-utd | . | . | . | . | . | 0.00 (7) | 0.00 (5) | 0.00 (5) | 0.00 (14) | 0.11 (9) | 0.00 (12) | 0.44 (9) | 0.58 (19) | 0.58 (12) | 0.96 (23) | 0.77 (13) | 1.00 (8) | 0.70 (23) | 0.89 (9) |
| SEB Sverige Indexfond | . | . | . | . | 1.00 (9) | 1.00 (6) | . | 1.00 (6) | 1.00 (9) | 1.00 (7) | . | 0.00 (5) | 0.00 (6) | 0.19 (16) | 0.07 (27) | 0.15 (13) | 0.00 (15) | 0.00 (21) | 0.00 (8) |
| SEB Sverige Indexnara | . | . | . | 0.75 (4) | 1.00 (12) | 0.00 (8) | 0.00 (7) | 0.00 (6) | 0.00 (16) | 0.00 (16) | 0.06 (16) | 0.00 (10) | 0.00 (6) | 0.00 (18) | 0.07 (27) | 0.00 (13) | 0.00 (15) | 0.00 (21) | 0.00 (8) |
| Skandia Sverige Exponering | . | . | . | . | . | 1.00 (6) | . | . | 1.00 (16) | 0.94 (16) | 0.38 (16) | 0.00 (10) | 0.00 (25) | 0.06 (18) | 0.00 (30) | 0.00 (13) | 0.00 (16) | 0.00 (6) | 0.00 (9) |
| Swedbank Robur Access Mix | . | 0.00 (6) | 0.00 (5) | 0.00 (6) | 0.00 (10) | 0.14 (7) | 0.00 (3) | 0.00 (6) | 1.00 (16) | 1.00 (13) | 0.81 (16) | 0.90 (10) | 1.00 (25) | 0.86 (14) | 0.93 (27) | 0.83 (12) | 1.00 (13) | 0.68 (22) | 0.83 (6) |
| Nordea Generationsfond 70-tal | . | 0.38 (8) | . | 0.00 (7) | 0.00 (9) | . | . | . | . | . | . | 0.57 (7) | 0.61 (18) | 0.67 (12) | 0.92 (13) | 0.77 (13) | 1.00 (7) | 0.70 (23) | 0.89 (9) |
| Nordea Donationsmedelsfonden | . | 0.25 (8) | . | 0.00 (7) | 0.00 (11) | 0.00 (8) | 0.00 (5) | 0.00 (5) | 0.00 (14) | 0.11 (9) | 0.00 (12) | 0.00 (8) | 0.50 (20) | 0.67 (12) | 0.96 (23) | 0.77 (13) | 1.00 (8) | 0.70 (23) | 0.89 (9) |
| KPA Blandfond | . | . | . | . | . | 0.17 (6) | . | . | . | . | 0.00 (5) | . | . | . | 0.00 (4) | 0.78 (9) | 0.91 (11) | 0.41 (17) | 1.00 (7) |
| Lansforsakringar Sparmal 2035 | . | 0.00 (3) | . | . | . | 0.67 (6) | . | 0.83 (6) | . | . | . | . | . | . | . | 0.25 (4) | 0.00 (4) | 0.70 (23) | 0.67 (9) |
| Swedbank Robur Access Edge Sweden | . | . | . | . | . | . | . | . | . | . | . | . | 1.00 (12) | 0.83 (6) | 0.75 (16) | 0.67 (9) | 0.75 (4) | 0.27 (11) | 1.00 (5) |
| Storebrand Sverige | . | . | . | . | . | . | 0.50 (4) | 0.83 (6) | 0.82 (11) | 0.44 (9) | 0.10 (10) | 0.22 (9) | 0.78 (23) | 0.47 (15) | 0.40 (25) | 0.31 (13) | 0.31 (16) | 0.30 (23) | 0.89 (9) |
| Nordea 2 SICAV BetaPlus EnhSwedish Sustainable Eq | . | . | . | . | . | . | . | . | . | . | . | . | . | . | 0.44 (9) | 0.11 (9) | 0.50 (12) | 0.17 (12) | 0.67 (3) |
| Handelsbanken Stiftelsefond | . | 0.75 (4) | . | 0.86 (7) | 0.00 (3) | 0.00 (4) | 0.00 (3) | 0.12 (8) | 0.17 (6) | . | . | . | . | . | . | . | . | . | . |
| Danske Invest Allocation Horisont Aktie | . | . | . | . | . | . | . | . | . | . | 0.07 (15) | 0.00 (10) | . | 0.88 (8) | . | . | . | 0.50 (4) | . |
