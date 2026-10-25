# thesis2/

Deep-research pass on thesis 2 (forced flows, Greenwood and Sammon anchor), 11 to 12 Oct 2026. Nothing older was deleted. Read in this order.

| file | what it is |
|---|---|
| `THESIS_IN_PLAIN_WORDS.md` | **Start here.** The thesis in plain words (25 Oct): what it is, what each section contains, which papers go where and what we take from each, how every table is built, who does what. Replaces `Thesis_in_plain_words.docx`. |
| `00_VALIDATION.md` | The verdict: does thesis 2 hold up against the blind referee, with the data found tonight. Two of three Friday gates met. |
| `01_DESIGN.md` | The pre-analysis plan: theory with equations (slow-moving capital price path, square-root impact law, dilution identity), four hypotheses each tied to one table, exposure measure, abnormal-return model, inference (cluster + wild bootstrap, Kolari-Pynnonen, randomisation within day), power with numbers, cost-benefit arithmetic, robustness. |
| `03_DATA.md` | What is on disk, what was found, and the three things you must do: pull the stock panel (LSEG or FinBas, exact field list), download ten FI zips (links), email Pensionsmyndigheten for sale dates (draft). |
| `outline/thesis2_outline.md` | Section-by-section outline with page budget (33 of 40), exhibits, equations, what each prize winner did in that section, and the trap per section. |
| `outline/winners_structure.md` | How the five closest prize winners are built: sections, pages, tables, hypotheses, theory, inference, conclusion. |
| `outline/requirements_checklist.md` | Every formal course requirement as a checklist. |
| `literature/literature_verified.md`, `references.bib` | 66 references, 52 verified, grouped by role in the paper, with magnitudes (Greenwood-Sammon by decade, Da et al., Hartzmark-Solomon 2025 AER, the grader's working paper). |
| `data/omxsb/` | OMXSB change list 2013-2026 (394 events, 325 verified) and OMXS30 2005-2026 (48), with notes, sources and build scripts. |
| `data/swing/` | Swing-pricing status at exit for the 78 FTN losers and the 60 largest 2019 exits, with sources. |
| `data/exit_days/` | Tranche days for the losers read from daily fund units and flows (no returns), plus the daily extract and the script. |
| `code/` | Event-study engine (tested), replication script, exposure and square-root prediction, power calculator, gated FTN scripts. |

The two-line summary: the design is buildable and better specified than before; the replication sample is OMXSB (394 events), the execution events are visible as one to three tranche days of 5 to 11 per cent of fund assets, and who-pays can be tested. The only blocking item is the stock-price panel, which is yours to pull this week.
