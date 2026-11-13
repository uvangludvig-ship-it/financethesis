# Finance thesis (BE451, hösten 2026)

## Valt thesis-ämne

**The Impact of the Swedish Fund Selection Agency (Fondtorgsnämnden) on the
Mutual Fund Market.**

- Författare: Ludvig Pauli Uväng och Alexander Fox.
- Önskad handledare: Michael Klug.
- Tentativ forskningsfråga: Hur har upphandlingen av premiepensionens
  fondtorg påverkat fondutbud, avgifter och kapitalflöden i Sverige, och har
  effekten spridit sig till fonder utanför PPM?
- Inlämnad synopsis: `synopsis/BScThesis_Fox_Pauli_Uvang.pdf`.

## Historiska vinnare

Den här mappen innehåller de historiska vinnarna i Stockholm School of
Economics officiella Primo-samling
[Awarded Bachelor Theses in Finance](https://hhs.primo.exlibrisgroup.com/discovery/collectionDiscovery?vid=46SSOE_INST%3A46SSOE_view&collectionId=8156252420006056&lang=en).

- Omfattning: 25 uppsatser, 2011–2024.
- Filer: `old_winners/`.
- Index och originalkällor: `old_winners/INDEX.md`.
- Kursmaterial och arbetsinstruktioner för BE451 hösten 2026:
  `course_context/README.md`.
- Verifiering: titel och författare har kontrollerats mot SSE-metadata och
  PDF-filerna. Samtliga 25 filer går att läsa som PDF (1 077 sidor totalt).

## Avgränsning

Urvalet bygger på medlemskap i SSE:s särskilda Finance-samling, inte på en
fri textsökning efter ordet `awarded`. Det fångar även äldre poster där ämne
och pris ligger i olika metadatafält.

SSE:s överordnade samlingssida visar samtidigt den äldre noteringen “No
theses awarded in 2024”. Finance-delsamlingen innehåller dock *The Smooth
Transition*, och dess egen post är uttryckligen märkt som 2024 års Per
Hiller-vinnare. Den är därför inkluderad.

En separat post från 2025, *Leading The Wallet*, har metadata som säger
“awarded ... 2026”, men ingår ännu inte i den officiella 25-posterssamlingen
för äldre Finance-vinnare och ligger därför inte i `old_winners/`.

## Icke-vinnande uppsatser (`non_winners/`)

Samtliga 635 kandidatuppsatser i finans i SSE:s bibliotekskatalog (taggade
"Bachelor Thesis in Finance", 2009–2026) som *inte* ingår i den prisbelönta
samlingen ovan. Hämtade 1 oktober 2026.

- `non_winners/INDEX.md` — tabell med år, titel, författare, sidantal, länk till
  originalet i SSE:s arkiv och länk till fulltexten.
- `non_winners/text/<MediumId>.txt` — fulltext för varje uppsats (layoutbevarande
  textextraktion ur arkivets PDF; 1801 och 2258 är OCR eftersom PDF:erna har
  trasig teckenkodning).
- `non_winners/catalogue_index.json` — rå katalogdata inkl. abstract för alla 660
  uppsatser (vinnare och icke-vinnare).
- `non_winners/extraction_meta.json` — sidantal, filstorlek och ordantal per uppsats.
- `non_winners/thesis_metrics.py` — skript som beräknar strukturmått (referenser,
  toppjournaler, introduktionslängd, metodnyckelord m.m.) ur textfilerna.
- `old_winners/text/` — fulltext för de 25 vinnarna, extraherad på samma sätt
  (2013 *Telling True from False* och 2020 *Chasing Your Own Tail* är OCR).

PDF-filerna (ca 1 GB) är inte incheckade; `non_winners/pdf/` ligger i `.gitignore`
och varje rad i indexet länkar till arkivets original.
