# Finance thesis BE451, hösten 2026: Alexander Fox och Ludvig Pauli Uväng

Handledare Michael Klug, examinator Riccardo Sabbatucci. Uppsats i Canvas och replikationspaket (zip) till Anneli Sandbladh **måndag 7 december kl. 10.00**. Presentation och opposition före 12 december, slutversion i Publish Thesis 18 december kl. 18.00.

## Börja här

**Uppsatsen vi skriver nu ligger i [`pagaende/03_omxsb_indexeffekt/`](pagaende/03_omxsb_indexeffekt/README.md).** Där gäller `thesis_final/`: kod, data och resultat som körs med en fil (`run_all.py`, sista raden ska vara `0 FEL`).

## Strukturen

Toppnivån är sorterad efter status. Varje uppsatsalternativ är en egen mapp med ett fast nummer och en `README.md` som säger vad som gäller, vad som är historik och var datan ligger. När ett alternativ byter status flyttas hela mappen; numret behålls.

```
pagaende/          det vi arbetar med nu
under_utredning/   nya alternativ som prövas (tom just nu; mall i README)
arkiv/             det som inte är aktuellt: tidigare alternativ och repots historik
data/              all data, gemensam för alla alternativ
reference/         kursmaterial, synopsis, vinnaruppsatser, kravlista
AI_LOG.md          kursens krav: varje AI-användning loggas samma dag
```

| Status | Mapp | Fråga | Ankare | När |
|---|---|---|---|---|
| **Pågående** | [`pagaende/03_omxsb_indexeffekt/`](pagaende/03_omxsb_indexeffekt/README.md) | Har indexeffekten försvunnit i Sverige? Replikation och utvidgning av G&S på OMXSB 2007–2026 | Greenwood & Sammon 2025 | 25 okt – |
| Under utredning | [`under_utredning/`](under_utredning/README.md) | – | – | – |
| Arkiv, vilande | [`arkiv/02_ftn_pristryck_gs_okt2026/`](arkiv/02_ftn_pristryck_gs_okt2026/README.md) | Pristryck när Fondtorgsnämnden tvingar fram försäljningar. Inga FTN-avkastningar har räknats; OMXSB-delen blev 03 | Greenwood & Sammon 2025 | 11–29 okt |
| Arkiv, övergivet | [`arkiv/01_ftn_tidiga_ankare_okt2026/`](arkiv/01_ftn_tidiga_ankare_okt2026/README.md) | Fondtorgsnämnden: flyttar FTN:s val privata pengar, och var premiepensionen trögare pengar? | Sialm–Starks–Zhang 2015 (vann ankartävlingen 5 okt), Cookson m.fl. 2021, Jenkinson–Jones–Martinez 2016, Da m.fl. 2018, Lou 2012/Wardlaw 2020 | 1–11 okt |
| Arkiv, avslutat | [`arkiv/00_amnesval_sep2026/`](arkiv/00_amnesval_sep2026/README.md) | Ämnesvalet inför synopsisen: ett tiotal kandidater. Synopsisen om Fondtorgsnämnden lämnades in 9 sep | olika | 6–9 sep |

Repots egen historik ligger i [`arkiv/repo_historik/`](arkiv/repo_historik/README.md): gamla startsidor, inventeringar, dubbletter och flyttkartan.

## Data: en gemensam mapp

All data ligger i [`data/`](data/README.md), en gång, och varje alternativ pekar dit. Rådata som PPM, FI, FTN och LSEG återanvänds mellan alternativen, och en fil på 1,3 GB ska inte finnas i flera kopior. `data/README.md` anger för varje datamapp vilket alternativ som använder den. `data/MANIFEST.md` beskriver varje fil.

Det enda undantaget är `pagaende/03_omxsb_indexeffekt/thesis_final/data/`. Den är en fryst kopia med md5 per fil, så att uppsatsen går att köra fristående och lämnas in som replikationspaket.

## Regler

1. **Repot ska vara privat.** Det innehåller licensierad data från LSEG, MSCI och SHoF.
2. **Inget raderas.** Det som inte längre är aktuellt flyttas till `arkiv/` eller till historiken i sin uppsatsmapp. Exakta dubbletter läggs i `arkiv/repo_historik/duplicates/` med en rad om var originalet finns.
3. **Allt ligger i git**, utom SHoF:s dagliga exporter (`data/raw/shof/Valuations/`, `Reinvestments/`). Filer över 50 MB går via Git LFS (`.gitattributes`). Kör `brew install git-lfs && git lfs install` en gång.
4. **Data:**
   - `data/raw/` ändras aldrig. Varje omvandling är ett skript i `data/build/`.
   - En ny datafil får en rad i `data/MANIFEST.md` samma dag, och en rad i `data/README.md` om den är en ny mapp.
   - Data som bara ett alternativ använder läggs ändå i `data/`, under ett tydligt namn, med alternativets nummer i kolumnen "Används av".
5. **AI får inte skriva uppsatstext** (kursregel). Allt AI-skrivet är underlag som författarna skriver om, och varje användning loggas i `AI_LOG.md`.
6. **Nytt alternativ:** `under_utredning/NN_kort_namn/` med nästa lediga nummer (04, 05 …) och en README enligt mallen i `under_utredning/README.md`. Mappen flyttas till `pagaende/` när ni bestämmer er och till `arkiv/` när den läggs ned.

## Var ligger det som låg i `code/`, `output/`, `thesis/`, `slides/` och `archive/`?

Varje fil som fanns före 13 nov 2026 och har flyttats står i [`arkiv/repo_historik/FLYTTKARTA_2026-11-13.tsv`](arkiv/repo_historik/FLYTTKARTA_2026-11-13.tsv) med gammal sökväg, ny sökväg och md5 (4 391 filer). Kortversion:

| Före 13 nov | Nu |
|---|---|
| `thesis_final/`, `thesis_draft_20261112/`, `thesis/literature/` | `pagaende/03_omxsb_indexeffekt/` (`litteratur/`) |
| `output/omxsb_*`, `code/claude_checks/`, `code/notebooks/`, `slides/`, OMXSB-skripten i `code/build/` | `pagaende/03_omxsb_indexeffekt/historik/` |
| `PLAN.md`, `STEPS.md`, `STATUS.md`, `thesis/design/`, `thesis/outline/thesis2_outline.md`, `thesis/research_2026-10-11/`, `thesis/text/`, `code/*.py` | `arkiv/02_ftn_pristryck_gs_okt2026/` |
| `archive/research_archive/`, `archive/literature_sweeps_2026-10/` | `arkiv/01_ftn_tidiga_ankare_okt2026/` |
| `archive/topic_selection_2026-09/`, `archive/agent_reports/`, `archive/synopsis_source/` | `arkiv/00_amnesval_sep2026/` |
| `code/build/` (dataskripten), `code/lseg/` | `data/build/` |
| `archive/` (resten) | `arkiv/repo_historik/` |
| `thesis/AI_LOG.md` | `AI_LOG.md` |
| `README.md` (startsidan till 4 nov) | `arkiv/repo_historik/old_readmes/README_rot_2026-11-04.md` |

Historiska skript är sparade exakt som de kördes och pekar därför på de gamla sökvägarna. Den levande koden körs från sina nya platser. Det gäller `thesis_final/`, `thesis_draft_20261112/`, `data/build/` och `arkiv/02_ftn_pristryck_gs_okt2026/kod/`, och den kontrollerades 13 nov.
