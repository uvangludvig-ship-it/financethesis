# Finance thesis BE451, hösten 2026: Alexander Fox och Ludvig Pauli Uväng

Handledare Michael Klug, examinator Riccardo Sabbatucci. Uppsats i Canvas och replikationspaket (zip) till Anneli Sandbladh **måndag 7 december kl. 10.00**. Presentation och opposition före 12 december, slutversion i Publish Thesis 18 december kl. 18.00.

Repot ordnades om **13 november 2026**: en mapp per uppsatsalternativ under `theses/`, och det som delas av alla (data, kursmaterial, AI-logg) ligger kvar i roten.

## Börja här

**Uppsatsen vi skriver nu är [`theses/03_omxsb_indexeffekt/`](theses/03_omxsb_indexeffekt/README.md).** Där gäller `thesis_final/`: kod, data och resultat som körs med en fil (`run_all.py`, sista raden ska vara `0 FEL`).

## Uppsatsalternativen

Varje mapp har en `README.md` som säger vad som gäller, vad som är historik och var datan ligger.

| Mapp | Fråga | Ankare | När | Status |
|---|---|---|---|---|
| [`theses/00_amnesval_sep2026/`](theses/00_amnesval_sep2026/README.md) | Ämnesvalet inför synopsisen: ett tiotal kandidatämnen (bl.a. A–K, private credit, tokenisering, Fondtorgsnämnden) | olika per ämne | 6–9 sep | **Avslutat.** Synopsis om Fondtorgsnämnden lämnades in 9 sep |
| [`theses/01_ftn_tidiga_ankare_okt2026/`](theses/01_ftn_tidiga_ankare_okt2026/README.md) | Fondtorgsnämnden: flyttar FTN:s val privata pengar, och var premiepensionen trögare pengar? | Sialm–Starks–Zhang 2015 (vann ankartävlingen 5 okt), Cookson m.fl. 2021, Jenkinson–Jones–Martinez 2016, Da m.fl. 2018, Lou 2012/Wardlaw 2020 | 1–11 okt | **Övergivet.** Ersatt av alternativ 02 den 11–12 okt |
| [`theses/02_ftn_pristryck_gs_okt2026/`](theses/02_ftn_pristryck_gs_okt2026/README.md) | Vad kostar det att flytta premiepensionen? Pristryck när FTN tvingar fram försäljningar | Greenwood & Sammon 2025 | 11–29 okt | **Vilande.** Inga FTN-avkastningar har räknats (`UNBLIND = False`). OMXSB-delen blev alternativ 03 |
| [`theses/03_omxsb_indexeffekt/`](theses/03_omxsb_indexeffekt/README.md) | Har indexeffekten försvunnit i Sverige? Replikation och utvidgning av G&S på OMXSB 2007–2026 | Greenwood & Sammon 2025 | 25 okt – | **AKTIV** |

Ett nytt alternativ får en ny mapp `theses/NN_kort_namn/` med en README enligt [`theses/MALL_README.md`](theses/MALL_README.md).

## Det som delas av alla alternativ

| Mapp eller fil | Innehåll |
|---|---|
| [`data/`](data/README.md) | All data: `raw/` (orörda källfiler), `input/` (handbyggda listor), `derived/` (det skript har tagit fram) och `build/` (koden som bygger eller hämtar datan). `data/README.md` visar vilket alternativ som använder vad; `data/MANIFEST.md` beskriver varje fil |
| [`reference/`](reference/README.md) | Kursmaterial, inlämnad synopsis, kravlista, vinnaruppsatser och vinnaranalyser |
| [`AI_LOG.md`](AI_LOG.md) | Kursens krav: varje AI-användning loggas samma dag |
| [`archive/`](archive/README.md) | Det som inte hör till något alternativ: gamla startsidor, inventeringar, dubbletter och flyttkartan |

## Regler

1. **Repot ska vara privat.** Det innehåller licensierad data från LSEG, MSCI och SHoF.
2. **Inget raderas.** Det som ersätts flyttas till historik eller `archive/`. Exakta dubbletter läggs i `archive/duplicates/` med en rad om var originalet finns.
3. **Allt ligger i git**, utom SHoF:s dagliga exporter (`data/raw/shof/Valuations/`, `Reinvestments/`). Filer över 50 MB går via Git LFS (`.gitattributes`). Kör `brew install git-lfs && git lfs install` en gång.
4. **`data/raw/` ändras aldrig.** Varje omvandling är ett skript i `data/build/` som skriver till `data/input/` eller `data/derived/`. En ny datafil får en rad i `data/MANIFEST.md` samma dag.
5. **AI får inte skriva uppsatstext** (kursregel). Allt AI-skrivet är underlag som författarna skriver om, och varje användning loggas i `AI_LOG.md`.
6. Varje alternativ har en README som säger vad som gäller. Den uppdateras när något nytt blir gällande.

## Var ligger det som låg i `code/`, `output/`, `thesis/` och `slides/`?

Varje gammal sökväg och dess nya sökväg finns i [`archive/FLYTTKARTA_2026-11-13.tsv`](archive/FLYTTKARTA_2026-11-13.tsv): 4 279 filer med md5. Kortversion:

| Före 13 nov | Nu |
|---|---|
| `thesis_final/`, `thesis_draft_20261112/` | `theses/03_omxsb_indexeffekt/` |
| `output/omxsb_*`, `code/claude_checks/`, `code/notebooks/`, `slides/`, OMXSB-skripten i `code/build/` | `theses/03_omxsb_indexeffekt/historik/` |
| `PLAN.md`, `STEPS.md`, `STATUS.md`, `thesis/design/`, `thesis/outline/thesis2_outline.md`, `thesis/research_2026-10-11/`, `thesis/text/`, `code/*.py` | `theses/02_ftn_pristryck_gs_okt2026/` |
| `archive/research_archive/`, `archive/literature_sweeps_2026-10/` | `theses/01_ftn_tidiga_ankare_okt2026/` |
| `archive/topic_selection_2026-09/`, `archive/agent_reports/`, `archive/synopsis_source/` | `theses/00_amnesval_sep2026/` |
| `code/build/` (dataskript), `code/lseg/` | `data/build/` |
| `thesis/literature/` | `theses/03_omxsb_indexeffekt/litteratur/` |
| `thesis/AI_LOG.md` | `AI_LOG.md` |
| `README.md` (startsidan till 4 nov) | `archive/old_readmes/README_rot_2026-11-04.md` |

Historiska skript är sparade exakt som de kördes och pekar därför på de gamla sökvägarna. Den levande koden körs från sina nya platser. Det gäller `thesis_final/`, `thesis_draft_20261112/`, `data/build/` och `theses/02_ftn_pristryck_gs_okt2026/kod/`, och den kontrollerades 13 nov.
