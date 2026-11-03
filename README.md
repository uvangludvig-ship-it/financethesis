<!-- OMXSB_CONTRIBUTION_ROUND_20261103 -->
> **Ny kapitaluppdelning, 3 november 2026:** [Resultat och beslut](output/omxsb_contribution_round_20261103/RESULTAT_OCH_BESLUT.txt) visar vilka nya respektive befintliga fondpositioner som bär kapitalförändringen i 98 tillägg med fasta kontroller. Fondantal och kapital ger olika rangordning av fondgrupperna. Separat omräkning bekräftar resultatet; prisets orsak är fortsatt öppen. Paketet innehåller också en stoppad riskdesign och rådatagranskningen av Runda11. [Körunderlag och publiceringsomfattning](output/omxsb_contribution_round_20261103/README.txt). Tekniskt forskningsmaterial, inte uppsatstext.

<!-- OMXSB_COMPLETE_OVERVIEW_20261102 -->
> **Samlad genomgång, 2 november 2026:** Läs först [kortversionen](output/omxsb_overview_20261102/LAS_FORST.txt) och sedan [hela sammanställningen](output/omxsb_overview_20261102/SAMMANFATTNING.txt). De täcker replikationen, alla identifierade senare analysfamiljer, Claudes runda6/runda7/MSCI, möjliga bidrag och konkreta förbättringar. [Filkartan](output/omxsb_overview_20261102/FILKARTA.txt) visar var materialet ligger. Äldre resultattexter är historik; bland annat T23b och MSCI har ännu orättade inferens-/datapunkter. Detta är beslutsunderlag, inte uppsatstext.

<!-- ANALYSIS_DELIVERY_20261102 -->
> **Senaste analyser, 2 november 2026:** Börja i `output/omxsb_broadening_20261102/RESULTAT.txt` för den senaste provningen, `output/omxsb_followup_20261102/RESULTAT.txt` för ägande/mängd/volym och `output/omxsb_open_questions_20261102/RESULTAT.txt` för daterade kontroller och prisförlopp. Prisets mekanism och långsiktiga varaktighet är fortfarande öppna. Se `PUBLICERING_20261102.txt` för licensierade råutdrag som stannar lokalt. Äldre struktur- och statusbeskrivningar nedan är historik.

> **Aktuell analysstatus, 1 november 2026:** Kontrollanalysen är rättad och dokumenteras i `output/omxsb_robusthet_20261101/RESULTAT.md`. Gällande OMXSB-arbetsstruktur finns i `thesis/design/OMXSB_struktur.md`. Den äldre FTN-beskrivningen nedan är historik och ingen genomförd extension. Inga FTN-utfall öppnas.

# Finance thesis (BE451, autumn 2026): Alexander Fox and Ludvig Pauli Uväng

**Topic (restated 29 Oct 2026):** Has the index effect disappeared in Sweden? A replication of Greenwood and Sammon (2025, JF) on OMXSB 2007-2026 that runs their tests of the five explanations for the disappearing index effect, and then runs the same test in a new setting: the forced sales after Fondtorgsnämnden's procurements, where the decision comes months before the sale and so separates predictability from event liquidity. Working title: "Pre-announced, uninformed, and large". The seminar deck is `slides/main.tex`. Tutor: Michael Klug. Examiner: Riccardo Sabbatucci.

## Start here

| File | What it is |
|---|---|
| `STATUS.md` | **Read first.** Where things stand today, next actions, open decisions, rules for agents |
| `PLAN.md` | The plan: question, parts and hypotheses, papers, specification, data, division of labour |
| `STEPS.md` | Seven gates and the week-by-week steps with owners and dates |
| `thesis/design/THESIS_IN_PLAIN_WORDS.md` | The thesis in plain words, section by section |
| `data/MANIFEST.md` | Every data file: what it is, where it came from, size, rows, who holds it |

## The five folders (restructured 27 Oct 2026)

Everything is sorted by role. One place per thing.

| Folder | What goes there | Never put here |
|---|---|---|
| `thesis/` | What the thesis **is**: design, outline, literature, LaTeX text, AI log | data, code |
| `code/` | **All** code: analysis scripts, build scripts, LSEG pulls, the notebook | data files |
| `data/` | `raw/` untouched inputs, `input/` hand-built lists, `derived/` what scripts produce | code, thesis text |
| `output/` | Tables, figures, numbers that go into the text | anything hand-edited |
| `reference/` | Course material, the submitted synopsis, prize-winning and non-winning theses | our own work |
| `archive/` | Topic selection (Sep to Oct), thesis 1, old summaries, duplicates. History only. | anything current |

Full map:

```
thesis/
  design/          00_VALIDATION, 01_DESIGN (pre-analysis plan), 03_DATA, THESIS_IN_PLAIN_WORDS, thesis2_method.tex/pdf
  outline/         section-by-section outline, winners' structure, requirements checklist
  literature/      66 references (52 verified), references.bib
  text/            main.tex and one file per section (to be written by the authors)
  research_2026-10-11/   the deep-research pass that chose this design
  AI_LOG.md        course requirement: every AI use
code/
  *.py             eventstudy (engine), replication_omxsb, pressure, power, ftn_eventstudy, dilution, parse_fi
  build/           scripts that build data/input and data/derived from data/raw
  lseg/            LSEG Workspace CodeBook pulls (v4 is current; old/ has v1-v3)
  notebooks/       replication_omxsb.ipynb: the OMXSB replication as run on 25 Oct (produced output/omxsb_replication/)
data/
  raw/ppm/         Pensionsmyndigheten monthly files 2001-2026, fund list, fees
  raw/ftn/         the 11 FTN procurement reports
  raw/fi/          FI quarterly holdings zips, all 31 quarters 2018Q4-2026Q2
  raw/shof/        SHoF fund master and field definitions; Valuations/ and Reinvestments/ are shared by hand (see MANIFEST)
  raw/lseg/        LSEG stock panels: panel_2012_2026, panel_2005_2026, panel_eu, datastream export
  input/           hand-built or hand-verified lists: OMXSB/OMXS30 events, swing-pricing status, LSEG request lists
  derived/         script outputs the analysis reads: PPM panel, FTN crosswalk and bids, exit days, measurements, facts, FI long
output/
  omxsb_replication/   events_car, nettrading, 36 tables, 6 figures, numbers.json (from the notebook)
  tables/NOTES.md      one sentence per thesis table, written when the table is done
reference/           course_context, synopsis, old_winners, non_winners, winners_analysis
archive/             topic_selection_2026-09, research_archive (incl. thesis 1), summaries, duplicates, inventory, tmp
```

## Rules

1. Nothing is deleted. Superseded material goes to `archive/`. Duplicates go to `archive/duplicates/` with their origin in the name.
2. Everything is in git, including data. Files over 50 MB go through Git LFS (`.gitattributes`); run `brew install git-lfs && git lfs install` once. The only files not in git are the SHoF daily exports (`data/raw/shof/Valuations/`, `Reinvestments/`), which are several GB.
3. `data/raw/` is never modified by hand or by code. Every transformation is a script in `code/build/` that writes to `data/input/` or `data/derived/`.
4. A new data file gets a row in `data/MANIFEST.md` the same day.
5. `PLAN.md` wins over every other file. `archive/` is history, not guidance.

## Key dates

- Full draft to Klug: **Fri 20 Nov**.
- Thesis in Canvas and replication zip to Anneli Sandbladh: **Mon 7 Dec, 10:00**.
- Presentation and opposition before 12 Dec. Publish Thesis by 18 Dec, 18:00.
