# Econometrics for Finance — Fall 2026

Originalfiler och praktiska anteckningar från Canvas-modulen
**Econometric Course**, kontrollerad den 3 september 2026 och
kompletterad den 30 september 2026.

## Originalfiler

- [Econometrics_Course.pdf](Econometrics_Course.pdf) — kursupplägg,
  programvarukrav, schema, stöd och källor; 3 sidor.
- [Lecture_1_Introduction_and_Cross_section_I.pdf](Lecture_1_Introduction_and_Cross_section_I.pdf)
  — materialet för pass 1 den 3 september; 83 fysiska PDF-sidor med
  Beamer-overlays, motsvarande 39 numrerade slides.
- [Lecture_2_Cross_section_and_IV.pdf](Lecture_2_Cross_section_and_IV.pdf)
  och [Lecture_2_Codes.zip](Lecture_2_Codes.zip) — pass 2, tvärsnitt och IV.
- [Lecture_3_Panel_Methods_and_DID_I.pdf](Lecture_3_Panel_Methods_and_DID_I.pdf)
  och [Lecture_3_Codes.zip](Lecture_3_Codes.zip) — pass 3, panelmetoder och
  difference-in-differences I.
- [Lecture_4_DID_II_Portfolio_sorts_and_Event_Study.pdf](Lecture_4_DID_II_Portfolio_sorts_and_Event_Study.pdf)
  och [Lecture_4_Codes.rar](Lecture_4_Codes.rar) — pass 4, DID II,
  portföljsorteringar och eventstudier.
- [All_slides_Fall_2026.pdf](All_slides_Fall_2026.pdf) — samtliga slides i
  en fil (uppladdad 22 september).
- [MANIFEST.md](MANIFEST.md) — Canvas-ID, storlek och SHA-256.

Den första föreläsningsfilen skapades av Morteza den 3 september 2026
kl. 10.35 och var publicerad i Canvas före dagens pass.

## Kursformat

- Fyra fysiska föreläsningar.
- Grundläggande ekonometriska begrepp och implementering i Python.
- Gemensam kodning och problemlösning; ta med laptop.
- Inga betygsatta uppgifter och ingen tentamen.
- Syftet är att ge en grund för den efterföljande uppsatsanalysen.
- Morteza erbjuder stöd i ekonometri och kodning under forskningsfasen.

## Schema

| Pass | Innehåll | Tid | Datum |
|---:|---|---|---|
| 1 | Introduction & Cross-section I | 13.15–15.00 | Torsdag 3 september |
| 2 | Cross-section II & IV | 15.15–17.00 | Tisdag 8 september |
| 3 | Panel Methods & Diff-in-Diff I | 13.15–15.00 | Tisdag 15 september |
| 4 | Diff-in-Diff II & RD; Portfolio Sorts & Event Study | 13.15–16.00 | Tisdag 22 september |

För pass 1 anger Canvas kalender:

- **Sal:** A342
- **Adress:** Sveavägen 65, tredje våningen
- **Tid:** 3 september, 13.15–15.00

Rum och eventuella schemaändringar ska alltid kontrolleras i Canvas/TimeEdit.
Pass 4 täcker fyra ämnen på mindre än tre timmar. Kursdokumentet säger att
portfolio sorts och eventstudier bara behandlas som grundrecept med
referenser; en uppsats som bygger tungt på någon av dem kräver egen
fördjupning.

## Förbered programvaran

Kursen är inte en programmeringskurs och installation görs inte på
lektionstid.

- Python 3.10 eller senare; Anaconda anges som enklaste helhetslösning.
- Paket: numpy, pandas, statsmodels, linearmodels och matplotlib.
- Med Anaconda behöver linearmodels normalt installeras separat.
- Editor: Jupyter Notebook, JupyterLab eller VS Code.
- Google Colab fungerar som installationsfri reservlösning, men lokal miljö
  rekommenderas för uppsatsarbete.
- Kontrollera att numpy, pandas, statsmodels och linearmodels kan importeras
  utan fel.

## Externa resurser i Canvas-modulen

- **Python Tutorial, QuantEcon:**
  https://python-programming.quantecon.org/intro.html
- **QuantEcon-källkod:**
  https://github.com/QuantEcon/lecture-python-programming
- **Introduktionsnotebook:**
  https://python-programming.quantecon.org/_notebooks/intro.ipynb
- **Boka tid med Morteza:**
  https://calendar.app.google/LYSaTCKFjGxYWeC67
- **Kontakt:** morteza.aghajanzadeh@hhs.se

Python-tutorialen är en extern webbplats, inte en Canvas-fil. Bokningssidan är
också en extern länk. Därför sparas de som länkar här i stället för att
kopiera hela tredjepartssidor.

## Pass 1: innehåll

Föreläsningen täcker:

- hur ett reproducerbart uppsatsprojekt bör organiseras;
- fyra frågor för forskningsdesign:
  1. vilken kausal relation är intressant?
  2. vilket idealexperiment skulle mäta effekten?
  3. vilken identifikationsstrategi används?
  4. hur görs statistisk inferens?
- forskningsprocessen som en iterativ kedja mellan fråga, data, rengöring,
  summering, analys och rapportering;
- kausal ordning, confounding, endogena/exogena variabler och SUTVA;
- potential-outcomes-ramverket;
- ATE, ATT och selektionsbias;
- OLS och Conditional Expectation Function;
- tolkning av regressioner;
- huvud- och interaktionseffekter;
- saturated models.

Huvudsammanfattningen är att observationsskillnaden i medelvärden består av
ATT plus selektionsbias, att forskningsdesignen behöver hitta en miljö där
selektionen elimineras, att OLS är den bästa linjära prediktorn och återger
CEF när denna är linjär samt att interaktioner ska inkludera motsvarande
huvudeffekter och tolkas försiktigt.

Följande nämns men behandlas inte i passet: Frisch–Waugh–Lovell, R²,
viktade regressioner/WLS, parameterrestriktioner, MLE, GMM, logit/probit och
normalisering. Nästa föreläsning ska behandla statistisk inferens och IV.

## Rekommenderad projektstruktur

Föreläsningen rekommenderar separata områden för:

- Literature — papers och rapporter;
- Data — raw och cleaned;
- Code — uppdelade och kommenterade skript;
- Meetings — sammanfattning, anteckningar och actions per möte;
- Doc — utkast och slides;
- Output;
- README.

## AI-notering

Pass 1 säger uttryckligen att AI-bilden innehåller Mortezas förslag och
**inte den officiella kurspolicyn**. Budskapet är att AI kan användas genom
forskningskedjan men aldrig ersätta studenternas forskning eller tänkande.
Kursöversikten säger dessutom att AI-svar måste kontrolleras mot betrodda
källor och att studenterna själva måste kunna förklara varje analyssteg.

Detta ändrar inte den försiktiga AI-regeln i huvud-[README](../README.md):
följ den officiella, strängare kursinformationen och be examinatorn om ett
skriftligt klargörande vid osäkerhet.

## Materialstatus 3 september

Canvas-modulen innehöll två nedladdningsbara filer: kursöversikten och
Lecture 1. Material för pass 2–4 var inte publicerat som egna filer vid
kontrollen. Modulen innehöll också Python- och bokningslänkarna ovan.

Den 30 september hade pass 2–4 (slides och kod) samt en samlad slidefil
publicerats; de ligger nu i mappen enligt listan ovan.

