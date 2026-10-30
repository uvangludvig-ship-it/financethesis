# PCA av forskningsarkitekturen i de 25 prisbelönta SSE-uppsatserna

Gjord 29 oktober 2026. Frågan: vad gör vinnarna gemensamt i hur de bygger upp sin uppsats, och hur skiljer det sig från de 635 övriga kandidatuppsatserna i finans 2009 till 2026? Analysen är kvantitativ och kompletterar närläsningen i `../winners_vs_nonwinners_analysis.md` och `../winners_audit.md`.

## Kort version

1. **Formen förklarar lite, designen förklarar mycket.** En klassificerare på 59 textmått skiljer vinnare från icke-vinnare med AUC 0,65 i korsvalidering. De två största principalkomponenterna i hela korpusen (ekonometrisk apparat respektive lärobokstruktur) skiljer inte alls vinnare från mängden. Vinnarna avviker på tre mindre komponenter: kvasiexperimentell identifiering (PC3), aktiv och resultatdriven text (PC4) och figurer plus siffror i stället för hedging (PC6).
2. **Det gemensamma mönstret, i mätbar form.** Vinnarna förhandsvisar resultatet i introduktionen ("we find", d = 0,61, p = 0,006), skriver i aktiv form ("We ..." inleder 6 % av meningarna mot 4 %, p = 0,015), hedgar mindre (2,6 mot 3,2 hedging-ord per 1 000 ord, p = 0,03), skriver nästan inga "limitation"-ord (0,08 mot 0,22 per 1 000, p = 0,016), har fler figurer (median 4 mot 2, p = 0,009), färre numrerade hypoteser, och sätter siffror i slutsatsen (1,7 mot 0,45 per 1 000 ord). Vinnarna är dessutom *mer homogena* än populationen på just dessa mått (spridningskvot 0,65 till 0,85), vilket är det starkaste tecknet på en delad norm.
3. **Vinnarna är inte en typ utan tre, och typerna är nästan kronologiska.** PCA på enbart vinnarna ger tre kluster: de tidiga encyklopediska naturexperimenten (2011 till 2013), de teoridrivna asset pricing-uppsatserna (2014 till 2018) och den moderna tabellreplikationen (2019 till 2024). Nio av elva i det moderna klustret replikerar en publicerad tabell och förlänger i en dimension. Det är det klustret en uppsats 2026 ska likna.
4. **Vad som är fritt.** Vinnarna varierar mer än populationen i reformvokabulär, siffror i slutsatsen, IV-vokabulär, meningslängd och antal referenser. Identifieringsstrategin och omfånget är alltså val, inte krav. Det som inte varierar är tonen och introduktionens uppbyggnad.

## 1. Data och metod

**Korpus.** De 25 vinnarna i `../../old_winners/text/` och de 635 icke-vinnarna i `../../non_winners/text/`, alla som `pdftotext -layout`-text. 52 icke-vinnare utesluts eftersom rubrikstrukturen inte gick att parsa (deras medianlängd är 12 700 ord, samma som de övriga, så bortfallet ser slumpmässigt ut). Kvar: 25 vinnare och 583 icke-vinnare.

**Egenskaper.** Skriptet `arch_features.py` beräknar 59 mått per uppsats, grupperade i:

- *Struktur*: andel av huvudtexten i introduktion, bakgrund/litteratur/hypoteser, data+metod, resultat+robusthet, diskussion+slutsats; antal huvudavsnitt; om det finns separata avsnitt för robusthet, hypoteser, diskussion, bakgrund. Rubrikerna identifieras automatiskt (numrerade, romerska, glesa versaler, tvåkolumnslayout) och sex vinnare har manuellt kontrollerade kategorier där parsern läste fel (listade i `OVERRIDE` i skriptet).
- *Introduktion*: längd, explicit fråga, resultatförhandsvisning, siffror med %/bps, citeringstäthet, bidragsformulering, disposition, ankarfraser.
- *Slutsats*: hedging, begränsningar, siffror, nollresultatspråk, citeringar.
- *Design- och inferensspråk per 1 000 ord*: ankarfraser ("we follow", "replicate"), bidrag, nollresultat, hedging, överdrivande ord, begränsningar, ekonomisk storlek, SE-rigor (clustered, Newey-West), identifieringsvokabulär (DiD, treatment, placebo), reform/tröskel-ord, "robustness", placebo, parallella trender, antal numrerade ekvationer, antal numrerade hypoteser.
- *Output och skrivande*: högsta tabell- och figurnummer, t-stat-täthet, citeringstäthet, referenslistans storlek, andel toppjournaler, webbkällor, "we"-täthet, andel meningar som börjar med "We", menings- och ordlängd, total längd, svensk kontext.
- *Metodvokabulär*: DiD, eventstudie, RD, IV, fixed effects, faktor/portföljsortering, enkät/kvalitativ, GARCH/VAR, ML.

Räknevariabler log-transformeras, alla variabler winsoriseras vid 1 och 99 procent, saknade värden ersätts med median, och allt standardiseras.

**Tre analyser.**

- A. *Kontrast per egenskap*: Cohen's d och Mann-Whitney-p för vinnare mot icke-vinnare, separat för hela perioden och för 2018 till 2024. Dessutom spridningskvoten (vinnarnas standardavvikelse delad med icke-vinnarnas), som mäter hur homogena vinnarna är.
- B. *Poolad PCA* på alla 608 uppsatser (10 komponenter) med vinnarna projicerade, samt en linjär diskriminant (LDA, shrinkage) i komponentrummet med femfaldig korsvalidering.
- C. *Vinnar-PCA* på 31 arkitekturmått för enbart de 25 vinnarna, följd av Ward-klustring på de fyra första komponenterna, korsad med de handkodade designvariablerna i `../winners_table.csv` (identifiering, tabellreplikation, resultatriktning).

Skript: `pca_winners.py`. Alla tabeller ligger i `data/`, figurerna i `fig/`.

## 2. Poolad PCA: var i rummet ligger vinnarna?

Variansen är spridd. Tio komponenter förklarar tillsammans 41 procent, den första 6 procent. Uppsatsarkitektur är alltså högdimensionell, och ingen enskild axel sammanfattar "en bra uppsats".

| Komponent | Varians | Vad den mäter (största laddningar) | Vinnare minus icke-vinnare (d) | p |
|---|---:|---|---:|---:|
| PC1 | 6,2 % | Ekonometrisk apparat och försiktighet: begränsningar i slutsats, fixed effects, "robustness", nollresultat, placebo, parallella trender | -0,05 | 0,66 |
| PC2 | 5,9 % | Lärobokstruktur: stor andel bakgrund/litteratur, många avsnitt, egna hypotes- och bakgrundsavsnitt, lång referenslista; *mot* ankarfraser, "we", toppjournalandel | -0,15 | 0,42 |
| **PC3** | 5,3 % | Kvasiexperimentell design: identifieringsvokabulär, DiD, parallella trender, reformord, längre intro; *mot* begränsningsprat och stor slutsats | **+0,46** | **0,03** |
| **PC4** | 4,3 % | Aktiv, lång, resultatdriven text: "we", "We"-meningar, referenser, ekvationer, tabeller, resultatförhandsvisning; *mot* hedging och stor intro | **+0,63** | **0,003** |
| PC5 | 4,0 % | Lång intro med bidragsformulering och många citeringar | +0,22 | 0,22 |
| **PC6** | 3,5 % | Figurer och siffror i slutsatsen; *mot* hedging, numrerade hypoteser, citeringstäthet | **+0,64** | **0,002** |
| PC7 till PC10 | 3,4 till 2,7 % | | 0,32 till 0,00 | > 0,25 |

Figur `fig/pooled_pc1_pc2.png` visar att vinnarna ligger utspridda i mitten av molnet på PC1 och PC2. Figur `fig/pooled_best_separation.png` visar PC4 mot PC6, där 20 av 25 vinnare ligger i den övre högra halvan.

**Tolkning.** Vinnarna har varken mer ekonometrisk apparat (PC1) eller mindre; de har inte mer lärobokstruktur (PC2). Det som skiljer dem är tre saker som alla handlar om *argumentets form*: en design med behandlade och obehandlade (PC3), en text som driver mot resultatet i aktiv form (PC4), och resultat visade som figurer och siffror i stället för hedgade meningar (PC6).

**Diskriminanten.** LDA på de tio komponenterna ger AUC 0,65 i korsvalidering. Det är bättre än slumpen men långt ifrån en klassificerare. De tyngsta vikterna i originalrummet är total längd (+), "we" (+), figurer (+), "We"-meningar (+), ordlängd (-), hedging (-), hedging i slutsats (-), resultatförhandsvisning (+), siffror i slutsats (+), tabeller (+). Vinnarnas egna rang på poängen går från plats 6 (2011 Hiller) till plats 583 av 608 (2015 Viotti), så vinnarskapet sitter inte i formen. Det bekräftar närläsningens slutsats: det är frågan, ankaret och identifieringen som avgör, och de syns bara delvis i textmått. Uppsats 6338, som katalogen flaggar som prisad 2026, hamnar på plats 161.

## 3. Kontrast per egenskap: det gemensamma mönstret

Sorterat på effektstorlek. Spridningskvot under 1 betyder att vinnarna är mer lika varandra än icke-vinnarna är.

| Egenskap | Vinnare (median) | Icke-vinnare (median) | d | p (alla) | p (2018 till 2024) | Spridningskvot |
|---|---:|---:|---:|---:|---:|---:|
| Resultat förhandsvisas i intro ("we find") | 100 % av vinnarna | 64 % | +0,61 | 0,006 | 0,049 | 0,82 |
| Begränsningsord per 1 000 | 0,08 | 0,22 | -0,52 | 0,016 | 0,046 | 0,68 |
| Andel meningar som börjar med "We" | 6,0 % | 3,9 % | +0,49 | 0,015 | 0,017 | 1,04 |
| Hedging-ord per 1 000 | 2,56 | 3,19 | -0,48 | 0,031 | 0,018 | 0,86 |
| Högsta figurnummer | 4 | 2 | +0,46 | 0,009 | 0,67 | 1,16 |
| Reform/regel/tröskel-ord per 1 000 | 0,24 | 0,19 | +0,44 | 0,40 | 0,93 | 2,29 |
| Ordlängd (bokstäver) | 4,92 | 5,03 | -0,44 | 0,038 | 0,60 | 0,90 |
| Begränsningar nämnda i slutsats | 0 | 0 | -0,41 | 0,07 | 0,12 | 0,67 |
| Hedging i slutsats per 1 000 | 6,0 | 7,0 | -0,39 | 0,09 | 0,085 | 0,88 |
| Numrerade hypoteser (tak 6) | 0 | 0 | -0,37 | 0,09 | 0,057 | 0,69 |
| Disposition i intro | | | +0,36 | 0,06 | 0,28 | 1,11 |
| Bidragsfraser per 1 000 | 0,075 | 0 | +0,34 | 0,05 | 0,16 | 1,12 |
| Siffror i slutsats per 1 000 | 1,71 | 0,45 | +0,30 | 0,08 | 0,22 | 1,81 |
| Siffror med %/bps i intro per 1 000 | 2,07 | 1,39 | +0,26 | 0,23 | 0,043 | 1,30 |
| Numrerade ekvationer | 4 | 2 | +0,23 | 0,23 | 0,048 | 1,12 |
| Vokabulär faktor/portföljsortering | 0 | 0 | -0,34 | 0,21 | 0,042 | 0,56 |
| Andel toppjournaler i referenser | 12 % | 16 % | -0,23 | 0,09 | 0,24 | 1,10 |

Fullständig tabell med 59 rader: `data/feature_contrast.csv`. Figur: `fig/feature_contrast.png`.

Vad som *inte* skiljer, återigen: total längd (13 400 mot 13 100 ord), antal avsnitt (7 mot 7), referenslistans storlek (38 mot 38), andel introduktion (10 mot 11 procent), andel resultat (23 mot 24 procent), t-stat-täthet, "robustness"-täthet, placebotest, SE-rigor. Strukturens *proportioner* är alltså inte hemligheten. Hemligheten sitter i vad som sägs i introduktionen och slutsatsen och i vilket register.

**Homogenitet som norm.** De mått där vinnarna är tightast (spridningskvot 0,65 till 0,80) är begränsningar i slutsats, begränsningsord, andel introduktion, numrerade hypoteser, intro-längd, t-stat-täthet, placebo och "robustness". Det är en gemensam *disciplin*: introduktionen är omkring 1 200 ord och 10 procent av texten, hypoteserna numreras inte, begränsningar listas inte, och ekonometrisk retorik hålls på en jämn nivå. De mått där vinnarna varierar *mer* än populationen (spridningskvot 1,4 till 2,3) är reformvokabulär, siffror i slutsatsen, IV, parallella trender, meningslängd. Det är de fria parametrarna: vilken identifiering man valt och hur kvantitativ slutsatsen är.

## 4. PCA på enbart vinnarna: tre arketyper

31 arkitekturmått, 25 uppsatser. De fyra första komponenterna förklarar 14, 13, 12 och 8 procent.

| Komponent | Positiv pol | Negativ pol |
|---|---|---|
| PC1 (14 %) | Kvasiexperiment: identifieringsvokabulär (+0,35), reformord (+0,34), nollresultatspråk (+0,32), lång intro (+0,30), stor intro-andel (+0,23) | Asset pricing-rigor: andel resultat (-0,29), SE-rigor (-0,28), ekonomisk storlek (-0,26), toppjournalandel (-0,21) |
| PC2 (13 %) | Omfång: total längd (+0,42), figurer (+0,36), referenser (+0,35), tabeller (+0,32), numrerade hypoteser (+0,27), hedging (+0,23) | Ankardriven: ankarfraser (-0,25), toppjournalandel (-0,23) |
| PC3 (12 %) | Intro som litteraturöversikt: citeringar i intro (+0,41), begränsningsord (+0,33), andel diskussion (+0,27), citeringstäthet (+0,23) | Intro som resultatförhandsvisning: "we find" (-0,37), andel resultat (-0,26), "we" (-0,21), meningslängd (-0,23) |
| PC4 (8 %) | Robusthetsavsnitt (+0,41), stor data+metod-andel (+0,38), begränsningsord (+0,29) | Ekonomisk storlek (-0,34), identifiering (-0,28), SE-rigor (-0,26), nollresultat (-0,26) |

Figur `fig/winners_pca.png` (biplot) och `fig/winners_loadings.png` (laddningar).

**Klustren** (Ward på PC1 till PC4, tre kluster):

| Kluster | Uppsatser | Median ord | Tabeller / figurer / referenser | Replikerar publicerad tabell | Ankarfraser /1k | Hedging /1k | Begränsningsord /1k | SE-rigor /1k | Toppjournalandel |
|---|---|---:|---|---|---:|---:|---:|---:|---:|
| 1. Modern tabellreplikation | 2013 Viotti, 2016 Hiller, 2019 Hiller, 2019 Viotti, 2020 Viotti, 2021 Viotti, 2022 Hiller, 2022 Viotti, 2023 Hiller, 2023 Viotti, 2024 Hiller | 11 300 | 5 / 3 / 27 | 9 av 11 ja | 0,33 | 1,5 | 0,00 | 0,00 | 15 % |
| 2. Tidiga encyklopediska naturexperiment | 2011 Hiller, 2011 Viotti, 2012 Viotti, 2013 Hiller | 23 000 | 11 / 11 / 95 | 0 av 4 | 0,09 | 3,3 | 0,06 | 0,05 | 2 % |
| 3. Teoridriven asset pricing och mekanism | 2014 Viotti, 2015 Hiller, 2015 Viotti, 2016 Viotti, 2017 Hiller, 2017 Viotti, 2018 Hiller, 2018 Viotti, 2020 Hiller, 2021 Hiller | 15 200 | 5,5 / 5 / 44 | 2 ja, 4 delvis, 4 nej | 0,12 | 4,0 | 0,20 | 0,67 | 9 % |

Resultatriktning per kluster: kluster 1 har 6 positiva, 4 blandade, 1 noll; kluster 2 har 4 blandade; kluster 3 har 7 positiva, 3 blandade.

**Kluster 1 är receptet.** Det är kort (11 000 ord), har få tabeller (5) och få referenser (27), men den högsta ankartätheten och den högsta andelen toppjournaler i referenslistan. Nio av elva replikerar en publicerad tabell (Petkova-Zhang, Adrian-Etula-Muir, English-Van den Heuvel-Zakrajsek, Kyle-Obizhaeva, Baek et al., Cieslak-Morse-Vissing-Jorgensen, Gabaix et al., Ahern-Dittmar) och förlänger sedan i en dimension: Sverige, en ny period, ett nytt tillgångsslag, en mekanism. Hedging är lägst (1,5 per 1 000 ord), begränsningsord är noll, och data+metod är den största sektionen (30 procent) följd av resultat (21 procent). Introduktionen är 1 300 ord med explicit fråga i 100 procent av fallen.

**Kluster 2 är historiskt.** Fyra uppsatser 2011 till 2013 på 23 000 ord med 95 referenser och elva tabeller. Höga reform- och identifieringsvärden (7,1 reformord per 1 000, tio gånger kluster 1). Ingen replikerar en tabell; alla fyra har blandade resultat. Ingen uppsats av den här typen har vunnit sedan 2013. Det är det formatet som uppsatsen i detta repo inte ska efterlikna, trots att det är lätt att tro att "mer" är bättre.

**Kluster 3 är mellanformen.** Asset pricing och mekanismtester 2014 till 2018 (plus 2020 Hiller och 2021 Hiller). Mest SE-rigor och ekonomisk-storlek-språk, mest hedging, största diskussionsandel (10 procent). Hälften replikerar delvis. Klustret delar ankarmönstret med kluster 1 men är 35 procent längre och mer försiktigt i tonen.

Klustren följer nästan tiden: 2 är 2011 till 2013, 3 är 2014 till 2018, 1 är 2019 till 2024. Det betyder att normen för vad som vinner har flyttat sig mot kompakt tabellreplikation med en förlängning, och det är den normen som gäller för en uppsats 2026.

## 5. Vad detta betyder för uppsatsen om Fondtorgsnämnden

Designen i `PLAN.md` (OMXSB-replikation av Greenwood & Sammon 2025 med Fondtorgsnämnden som ny miljö) är exakt kluster 1: en publicerad tabell replikeras, och förlängningen är en ny institutionell miljö. Det som återstår är att skriva den i kluster 1-register. Målvärden hämtade från klustrets medianer:

| | Mål (kluster 1-median) | Varför |
|---|---|---|
| Total längd | 11 000 till 13 000 ord | Kluster 2-längd (23 000) har inte vunnit sedan 2013 |
| Introduktion | 1 200 till 1 400 ord, 10 till 12 % | Explicit fråga, "we find" med siffror (två till tre tal med % eller bps), ankarpapper nämnt, bidrag i en mening |
| Data + metod | ~30 % | Största avsnittet i kluster 1; det är där replikationen görs trovärdig |
| Resultat + robusthet | 21 till 25 % | Robusthet inne i resultatavsnittet, inte som eget efterhängt avsnitt |
| Diskussion + slutsats | ~10 % | Siffror i slutsatsen (1,7 per 1 000 ord), inga listade begränsningar, inga "limitation"-ord |
| Tabeller / figurer | 5 till 6 / 3 till 4 | En huvudtabell som ställs mot ankarets tabell siffra för siffra |
| Referenser | 25 till 40, 15 % toppjournaler | Korta, riktade; ingen lärobokslitteratur |
| Numrerade hypoteser | 0 | Vinnarna formulerar en fråga, inte H1 till H5 |
| Hedging | under 2 per 1 000 ord | "may", "might", "tendency", "seems" ersätts av ett tal och ett konfidensintervall |
| Aktiv form | "We" inleder ~6 % av meningarna | Argumentet drivs av författarna, inte av litteraturen |

## 6. Förbehåll

- 25 vinnare är få. Effekter under d = 0,4 är inte signifikanta och klustren är beskrivande, inte testade.
- Textmåtten är proxyvariabler. "Hedging-ord" fångar register, inte om slutsatsen faktiskt är välkalibrerad. Figurnummer fångar hur många figurer som refereras i löptext.
- Rubrikparsningen är automatiserad för icke-vinnarna. 52 av 635 föll bort, och för de övriga finns felklassificeringar av enskilda avsnitt som inte är kontrollerade för hand. Vinnarnas avsnitt är kontrollerade.
- Metodvokabulär och referensmått är korrelerade med ämne och årtal. Kluster 2:s höga referensantal är delvis en 2011-norm.
- Den poolade PCA:n förklarar 41 procent av variansen med tio komponenter. Det är väntat för 59 heterogena mått, men det betyder att enskilda komponenter ska läsas som tendenser.

## Filer

| Fil | Innehåll |
|---|---|
| `arch_features.py` | Egenskapsextraktion från text (59 mått), inklusive rubrikparser och vinnar-overrides |
| `pca_winners.py` | Kontrast, poolad PCA, LDA, vinnar-PCA, klustring, figurer |
| `data/arch_features_all.csv` | 660 rader, alla råmått |
| `data/feature_contrast.csv` | Vinnare mot icke-vinnare per mått: medianer, d, p, spridningskvot |
| `data/pooled_loadings.csv`, `data/pooled_scores.csv`, `data/pooled_pc_contrast.csv` | Poolad PCA |
| `data/winner_direction_feature_weights.csv`, `data/winner_likeness_scores.csv` | LDA-riktning och poäng per uppsats (korsvaliderad) |
| `data/winners_loadings.csv`, `data/winners_scores_clusters.csv` | Vinnar-PCA och kluster med handkodade designvariabler |
| `fig/` | `pooled_pc1_pc2.png`, `pooled_best_separation.png`, `scree_pooled.png`, `feature_contrast.png`, `winners_pca.png`, `winners_loadings.png` |

Reproduktion, från `reference/`:

```
python3 -I winners_analysis/pca/arch_features.py winners_analysis/pca/data/arch_features_all.csv old_winners/text non_winners/text
python3 -I winners_analysis/pca/pca_winners.py winners_analysis/pca/data/arch_features_all.csv winners_analysis/winners_table.csv winners_analysis/pca
```
