# AP- och FI-insamling 2026-10-31

Insamlingen är delvis komplett: 66 av 112 efterfrågade fond/datum-kombinationer har innehavsdata. CSV-filen innehåller 10,444 rader. Inga datum har fyllts ut med närliggande observationer och frånvaro av en lista betyder inte noll innehav.

| Fond | Hämtade halvår | Saknade publicerade perioder |
|---|---:|---|
| AP1 | 2: 2025-06-30, 2025-12-31 | Båda halvåren 2013–2024 |
| AP2 | 22: 2015-06-30–2026-06-30, utom 2017-12-31 | Båda halvåren 2013–2014 samt 2017-12-31 |
| AP3 | 19: 2017-06-30–2026-06-30 | Båda halvåren 2013–2016 |
| AP4 | 23: 2015-06-30–2026-06-30 | Båda halvåren 2013–2014 |

AP1:s verksamhet upphörde 2025-12-31 enligt [AP4:s AP1-arkiv](https://www.ap4.se/om-ap4/om-ap1/); 2026 markeras därför som ej tillämpligt. För AP2–AP4 är 2026-12-31 ett framtida rapportdatum, inte en redan förfallen publicering. Totalt: 40 äldre listor ej funna, 1 felaktigt daterad arkivlänk, 2 ej tillämpliga fond/datum och 3 framtida datum.

## Filer och spårbarhet

- `AP1/`–`AP4/`: oförändrade PDF-original, inklusive utländska aktielistor när fonden publicerar dem separat. 110 innehavsfiler sparades, varav 107 avser efterfrågade halvår. Tre extra filer från AP2 (2018-03-31 svenska/utländska samt 2024-04-04 utländska) ligger kvar som dokumentation av arkivets länkar och används inte i CSV-filen. AP4:s årsredovisning 2014 sparades också för kontroll; den innehåller endast största innehaven och används inte som ersättning för en fullständig lista.
- `download_log_2026-10-31.csv`: samtliga HTTP-hämtningar/försök och FI:s lyckade webbläsarhämtning, med URL, nedladdningstid i UTC, lokal sökväg, storlek, SHA-256 och eventuellt fel.
- `_collection_20261031/requests.jsonl`: löpande maskinläsbar logg. HTML-sidor och dokumentlänkar sparas bredvid den.
- `_collection_20261031/coverage.csv`: exakt en rad för var och en av de 112 efterfrågade kombinationerna. `missing_lists.csv` innehåller de 46 som inte har data.
- `../../derived/ap/ap_svenska_aktier_2013_2026.csv`: de sex efterfrågade kolumnerna. **Marknadsvärde anges i SEK**, omräknat från källans kr/TSEK/MSEK. Antal aktier är källans antal, utan splitjustering. Decimaltecken är punkt; CSV-avgränsare är komma; UTF-8 med BOM.
- `../../derived/ap/ap_svenska_aktier_med_ric.csv`: samma rader med RIC, osäkerhetsflaggor, käll-URL, PDF-sida och rad, källenhet och klassificeringsgrund.
- `../../derived/ap/matchningar_att_granska.csv`: alla osäkra eller omatchade rader, inklusive eventuella RIC-förslag.
- `../../derived/ap/excluded_rows.csv`: bortvalda utländska innehav, rättigheter, privata kreditfonder/skuldebrev och bolagssummor som annars skulle dubbelräknas med aktieslagsrader. Tomma ISIN har aldrig ersatts med ett påhittat värde.

## Definition och begränsningar

”Svenska aktier” tolkas som svenska aktiemarknaden, inklusive utländska emittenter noterade i Sverige. Urvalet utgår från fondernas svenska aktielistor/Sverige-avsnitt. Identifierade avvikelser (Spotify, Polestar ADS, Domtar och Restaurant Brands) har lyfts bort; de redovisas med primärkällor i `classification_sources.csv`. Det är inte en oberoende historisk noteringsdatabas: källornas kvarvarande nollvärdesinnehav behålls och flaggas för granskning av noteringsstatus.

AP1 har inga marknadskoder: svenska ISIN används, kompletterat med utländska ISIN som samma datum förekommer i övriga fonders svenska listor. Dessa utländska AP1-rader flaggas särskilt; samma ISIN kan handlas på flera marknader och AP1:s exakta handelsplats kan inte avgöras ur filen.

AP2 anger på många listor att innehaven är **netto efter utlånade aktier**. Därför är AP2:s antal inte utan vidare jämförbara med bruttoägande hos andra fonder. Källvärden har inte justerats för värdepappersutlåning.

AP4 redovisar ibland aktieslag samlat (särskilt 2019-12-31 och 2023-12-31). Sådana rader behålls, med `samlat_aktieslag=true` och tom RIC. Sammanskrivna ISIN bevaras i `kall_ISIN` men inte som ett falskt enskilt ISIN i huvudkolumnen. När källan visar både bolagssumma och aktieslag används endast aktieslagen.

## RIC-matchning

Eventkälla: `data/input/omxsb/omxsb_events_with_ric_2007_2026.csv`. Exakt ISIN prioriteras. Där eventlistan saknar ISIN används de befintliga LSEG-filerna `panel_2012_2026/stocks_static.csv` och `panel_2005_2026/stocks_static_2005.csv`, endast för RIC som faktiskt finns i eventlistan.

Namn normaliseras för versaler, diakritik, skiljetecken och bolagssuffix; aktieslag bevaras. En entydig exakt normaliserad namnmatch kan få RIC men är **alltid flaggad som osäker**. Bolagsmatch utan säkert aktieslag, identifierarkonflikt och ungefärlig namnmatch ger endast kandidater, ingen automatisk RIC. RIC för flera aktieslag fördelas aldrig på en samlad innehavsrad. Eventlistan är inte ett fullständigt börsregister; många stora permanenta indexmedlemmar saknar därför match.

4,412 rader har ifylld RIC, varav 3,411 har entydig identifierarmatch. Övriga 7,033 rader är flaggade för osäker match eller saknad eventmatch. `osaker_matchning=false` avser identitetsmatchen, inte en oberoende kontroll av historisk handelsplats eller noteringsstatus.

## Kontroller

Alla sparade original har verifierats mot nedladdningshash. Datum läses ur PDF-innehållet. Noll felaktigt tolkade kandidatrader återstår, inga dubbletter av fond/datum/ISIN finns och inga negativa antal eller marknadsvärden förekommer. AP4:s 23 svenska delsummeringar stämmer inom den högsta möjliga effekten av källans avrundning. AP4 2026-06-30 har grafiska rubriker och summa som saknas i textlagret; summan 144 755 MSEK och avgränsningen till sidorna 1–3 har kontrollerats visuellt. Kontrollbilden sparas i `_collection_20261031/ap4_2026_p3.png`. Representativa sidor för AP1, AP2, AP3 samt äldre och nyare AP4 har också granskats visuellt.

`source_checks.csv` visar summering före instrument-/marknadsurval, för jämförelse med originalets svenska avsnitt (för AP1 samtliga lästa aktier). Där källan saknar totalsumma lämnas kontrollen tom. Full kontrollsammanställning finns i `_collection_20261031/validation_summary.json` och `source_total_validation.csv`.

## FI

Original: `../fi_short/HistoriskaPositioner_2026-10-31.ods`. FI:s nuvarande exportformat är ODS, trots att sidan kallar filerna Excelfiler. Den sparade filen är en verifierad ODS med 39,061 positionsrader och positionsdatum 2010-05-10–2026-10-30. Äldre datum är datumceller medan nyare ofta är textceller; originalformatet har bevarats.

Direkta HTTP-försök mot exportadressen gav 404. Hämtning via knappen ”Historiska positioner” på [FI:s register](https://www.fi.se/sv/vara-register/blankningsregistret/) i Chrome lyckades; den filen har kopierats byte för byte till repot. Filen avser offentliga betydande korta nettopositioner, inte samtliga rapporterade småpositioner; `<0,5` är en rapporterad tröskelpassage och inte nödvändigtvis noll.

## Sökta luckor och reproduktion

AP1:s aktuella domän och tidigare innehavssida leder nu till AP4:s information med listor för 2025. Den äldre officiella CDN-domänen kunde inte DNS-upplösas. AP2:s offentliga dokumentindex för 2013 och 2014 innehöll rapporter men inga innehavslistor. AP3:s aktuella innehavsarkiv börjar 2017. AP4:s årssökning 2014 gav inga innehavslistor; årsredovisningen hänvisar till en separat fullständig lista men visar själv endast fem största. Kompletterande webbsökningar efter respektive fonds äldre listor gav inga ytterligare fullständiga original på fondernas nuvarande webbplatser. Saknade perioder har inte ersatts med sammanfattningar eller tredjepartsrekonstruktioner.

Insamlingen har endast skrivit nya filer under `data/raw/ap`, `data/raw/fi_short`, `data/derived/ap` och nya fristående skript i `code/build`. Befintliga källfiler har enbart lästs. Andra pågående arbeten i det gemensamma repot har inte ändrats eller återställts.

Extraktionen kan upprepas utan nätverk med `python3 code/build/parse_ap_20261031.py --out /tmp/ny_tom_katalog` (Poppler/pdftotext krävs). Alla utdata skrivs exklusivt; välj en sökväg som inte redan finns. Hämtaren och slutkontrollen har tidsstämplade namn i `code/build`. FI-hämtningen kräver webbplatsens knapp om den direkta exportadressen fortsatt ger 404.
