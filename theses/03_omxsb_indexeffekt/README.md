# 03 Har indexeffekten försvunnit i Sverige? OMXSB 2007–2026

**Status:** AKTIV. Det här är uppsatsen vi skriver.
**Senast ändrad:** 12 nov 2026: `thesis_final` (Alexander, tabell A6, 12 nov 11:11) och `thesis_draft_20261112` (12 nov 16:39). Mappen samlades här 13 nov 2026.

## Frågan

En replikation och utvidgning av Greenwood & Sammon (2025, *Journal of Finance* 80(2), 657–698), "The Disappearing Index Effect", på alla tillägg och borttag i OMXSB 2007–2026: 536 händelser och 39 översyner. Har priseffekten av indexändringar minskat i Sverige, och vad ligger bakom? Utvidgningarna gäller:
- indexfondernas köp (D) och priset per köpt procent (M),
- vem som köper,
- överlapp med MSCI Sweden,
- händelser med egen bolagsnyhet,
- sammansättning och uppgång före beskedet,
- likviditet,
- nyemissioner och OMXS30,
- extremvärden,
- nästan tillagda aktier,
- återgång,
- A/B-tvillingar.

Uppsatsen växte ur del 1 av oktoberplanen (alternativ 02). FTN-delen ingår inte.

## Det som gäller

| Vad | Var | Kommentar |
|---|---|---|
| **Kod, data och resultat** | [`thesis_final/`](thesis_final/README.md) | Steg 01–16 och en fil per tabell och figur (`code/output/`). `run_all.py` kontrollerar indata mot md5, kör allt och slutar med `0 FEL` när huvudsiffrorna är desamma som i testet. Alla tabeller och figurer i Word: `results/tables/` (`all_tables.docx`, `all_tables.pdf`). Deklarationer skrivna före körningarna: `declarations/`. Alexander äger koden |
| **Utkast till text (AI-genererat)** | [`thesis_draft_20261112/`](thesis_draft_20261112/README.md) | Engelskt arbetsutkast, "The Index Effect in Sweden" (Word, PDF, LaTeX), med granskningsrapporter och en fryst kopia av `thesis_final` från commit `d2d4166`. **Underlag, inte uppsatstext:** kursen förbjuder AI-skriven text, så ni skriver texten själva |
| **Litteratur** | [`litteratur/`](litteratur/) | `references.bib` (senast ändrad 9 nov) och `literature_verified.md` (verifierad lista från 12 okt) |
| **AI-logg** | [`../../AI_LOG.md`](../../AI_LOG.md) | Kursens krav. Gäller alla alternativ |

## Hur man kör

```
cd theses/03_omxsb_indexeffekt/thesis_final
pip install pandas==3.0.5 numpy==2.5.3 scipy==1.18.1 python-docx==1.2.0 matplotlib==3.11.2
python3 run_all.py          # cirka 10 minuter, sista raden ska vara "0 FEL"
```

Kontrollerat 13 nov 2026 på en kopia utanför repot med pandas 2.2.3, numpy 1.26.4 och scipy 1.15.2: `0 FEL`. Kör man i mappen skrivs `results/` om, och `results/` ligger i git.

## Data

`thesis_final/data/` är en fryst kopia av allt steg 01–16 läser. Varje fil har en md5-summa i `thesis_final/data/FILES.csv`. Kolumnen `original_path` där anger var filen låg **före** 13 nov. Den nya platsen slår man upp i `archive/FLYTTKARTA_2026-11-13.tsv`. Källorna i den gemensamma `data/` är främst:
- `data/raw/lseg/panel_2005_2026/` (kurspanelen; `stocks_daily_2005.parquet` är samma data som `thesis_final/data/prices/all_stocks_daily_*`),
- `data/input/omxsb/` (händelselistorna med Nasdaqs besked),
- `data/raw/lseg/klassificering/`,
- `data/raw/lseg/twins/`.

Övrig indata kommer från Claude-rundorna och 2007-körningen i `historik/`.

## Historik (gäller inte)

Allt OMXSB-arbete före `thesis_final` ligger i [`historik/`](historik/README.md), ett paket per körning med sitt ursprungliga namn. Tabellen där visar för varje paket vad det gjorde, vad det kom fram till och om det används i `thesis_final`. Kortversion:

- **25–31 okt:** första replikationen (2013–2026, notebook) och 2007–2026-körningen med G&S fem förklaringar. 2007-körningens CAR och strykningsflaggor är indata till `thesis_final`.
- **1–5 nov:** Claude-rundorna 2–12 i `historik/claude_checks/`. Därifrån kommer större delen av `thesis_final/data/` och koden för steg 07 och 10–16.
- **31 okt – 4 nov:** ett tjugotal utforskande paket om ägare, volym, auktioner, SHoF-data och historik före 2007. Designomprövningen 4 nov (`historik/omxsb_design_reset_20261104/LAS_FORST.txt`) konstaterade att inget av dem identifierar prisets orsak. Inget av dem ingår i `thesis_final`.

`thesis_final/README.md` säger under "Det som inte är med här" att kontrollgrupperna, återgången, tvillingarna och förutsägbarheten körs från gamla skript i `historik/claude_checks/`. Sedan dess har steg 14 (nästan tillagda), 15 (återgång) och 16 (tvillingar) lagts till, så meningen är delvis inaktuell. Förutsägbarheten (runda 6) har inget eget steg i `thesis_final`.

Grenen `origin/slides-seminar-deck` har en commit som inte är mergad: Alexanders seminariedeck från 29 okt. Decket som ligger i `main` finns i `historik/slides_seminarium_20261029/`.
