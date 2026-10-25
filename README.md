# Finance thesis (BE451, autumn 2026): Alexander Fox and Ludvig Pauli Uväng

**Topic (thesis 2, from 12 October):** "Pre-announced, uninformed, and large: the price of moving the premium pension". The price pressure of Pensionsmyndigheten's forced sales after Fondtorgsnämnden's procurements, anchored on Greenwood and Sammon (2025, JF) and replicated on OMXSB. Tutor: Michael Klug. Examiner: Riccardo Sabbatucci.

## Start here

| File | What it is |
|---|---|
| `STATUS.md` | **Read first.** Where things stand today: done, next actions, open decisions, rules for agents |
| `PLAN.md` | **The plan.** Question, parts and hypotheses, papers, specification, data, division of labour, working rules, risks |
| `STEPS.md` | Seven gates and the week-by-week steps with owners and dates |
| `thesis2/` | The thesis: design (`01_DESIGN.md`), method note (`thesis2_method.tex`), outline, code, derived data, literature, text, AI log |
| `research/reference/` | Evidence that still guides the writing: winners vs non-winners, how winners write conclusions |
| `research/_archive/` | Everything superseded, including thesis 1 (the SSZ plan) and the 11 Oct transition folder. History only |

## Folder map

| Folder | Contents |
|---|---|
| `thesis2/code/` | Analysis code (`code/README.md` gives the run order and the unblinding switch) |
| `thesis2/data/` | Event lists (OMXSB, OMXS30), tranche days, swing-pricing status, LSEG input lists; `prices/raw/` holds the licensed Datastream pull and is not in git |
| `thesis2/output/` | Script outputs; `tables/` holds the `.tex` fragments the text includes |
| `thesis2/text/` | LaTeX, one file per section |
| `thesis2/research/` | The 11-12 Oct deep-research pass that chose thesis 2 (question map, anchors, blind referee, proposal) |
| `data/raw/` | Pensionsmyndigheten monthly files 2001-2026 (raw, untouched) |
| `data/Valuations/`, `data/Reinvestments/` | SHoF Morningstar daily exports (not in git; from SHoF) |
| `data/panel/`, `data/measurements/`, `data/facts/`, `data/winners/`, `data/agent_reports/` | Derived PPM panel 2018-2026, FTN round membership and measurements, sourced institutional facts |
| `data/derived/` | SHoF monthly series; FTN bids, fees and the PPM-SHoF crosswalk (`ftn_2026-10-11/`) |
| `data/FTN/` | The 11 FTN procurement reports |
| `data/extra/` | FI holdings zips, selected PPM workbooks, SHoF fund master and field definitions |
| `course_context/` | Syllabus, synopsis instructions, econometrics slides, checklist |
| `synopsis/` | Submitted synopsis (`BScThesis_Fox_Pauli_Uvang.pdf`); its question predates thesis 2 |
| `old_winners/`, `non_winners/` | The 25 awarded SSE finance theses and the non-winner corpus, with indexes |

## Key dates

- Full draft to Klug: **Fri 20 Nov**.
- Thesis in Canvas and replication zip to Anneli Sandbladh: **Mon 7 Dec, 10:00**.
- Presentation and opposition before 12 Dec. Publish Thesis by 18 Dec, 18:00.

## Not in git

`data/Valuations/`, `data/Reinvestments/`, `thesis2/data/prices/` (licensed; shared by hand) and build files. See `.gitignore`.

Last tidied: 25 October 2026.
