# STEPS.md: gates, steps and dates

Companion to `PLAN.md`. Written 25 October 2026. Six weeks to the hard deadline (Mon 7 Dec, 10:00). The schedule puts the full draft at Fri 20 Nov, which leaves two weeks for Klug's comments, an outside read, the number audit and the package.

Two tracks (`PLAN.md`, section 6): **L** = Ludvig (data, code, exhibits, package), **A** = Alexander (correspondence, text, literature, AI log, seminar deck). Each step has an owner. "Both" means a call or a sitting together.

---

## The seven gates

| # | Gate | Passed when | Target |
|---|---|---|---|
| 1 | **Repo clean and shared** | Repo private; cleanup pushed; L has a clone and the licensed folders by hand from A; both can run `python3 thesis2/code/eventstudy.py` (self-test) | Mon 26 Oct |
| 2 | **Panel in the code's format** | `stocks_daily.csv`, `stocks_static.csv`, `indices_daily.csv`, `factors_daily.csv` exist; all 394 OMXSB events map to a series with prices around their dates; FI zips on disk | Fri 30 Oct |
| 3 | **Table 2 run** (first unblinded result, no FTN date) | `replication_omxsb.py` runs end to end; one-sentence reading written; dose and MDE recomputed on actual ADV | Sun 1 Nov |
| 4 | **Klug sign-off, unblinding** | Written yes on the specifications and the five open decisions; date written in `thesis2/03_DATA.md` E; `UNBLIND = True` in the same commit | Fri 6 Nov |
| 5 | **Data freeze and all main results** | SHoF refresh to 31 Oct in; small-cap tranches dated; Tables 3, 4, 5 run as registered | Fri 13 Nov |
| 6 | **Full draft to Klug** | Every claim traces to a table cell or a cited page; clean-machine run from raw data; 33 pages or fewer | Fri 20 Nov |
| 7 | **Submission** | Outside read done and fixed; number audit; AI appendix; replication zip; two proofreads, one on paper | Ready Fri 4 Dec; submit Mon 7 Dec 10:00 |

---

## Steps, in order

### Week 1 (Mon 26 Oct to Sun 1 Nov): panel and Table 2
- [ ] **Mon 26 [A]:** make the GitHub repo private; `git push`; empty `~/Documents/_to_delete/` after a glance. **Gate 1.**
- [ ] **Mon 26 [L]:** clone; get `data/Valuations`, `data/Reinvestments`, `thesis2/data/prices/raw` from A by hand; run the `eventstudy.py` self-test. Read `00_VALIDATION.md`, `01_DESIGN.md`, `thesis2_method.pdf`, the outline.
- [ ] **Mon 26 [A]:** email Klug: the method note as PDF, one paragraph on what changed since the synopsis, a meeting request for the week of 2 Nov with the five decisions. Email Pensionsmyndigheten (draft in `03_DATA.md` C, in your own words). Open `thesis2/AI_LOG.md` and add the entries you know of.
- [ ] **Mon 26 to Wed 28 [L]:** build the panel. Re-run the Datastream list with a code row (RIC or ISIN), `MV`, `NOSH`, and pull the five index series. Write `thesis2/code/build_prices.py`: wide to long, `volume_sek = VO x 1000 x P`, static table (id, name, ticker, isin, first and last date), drop the 30 `#ERROR` series and list them. Match the 394 events; hand-resolve the unmatched file. **Gate 2.**
- [ ] **Tue 27 [L]:** download the 13 FI zips (`03_DATA.md` B); `parse_fi.py`; check the nine foreign losers without holdings.
- [ ] **Tue 27 to Thu 29 [A]:** institutional background (2.5 pages) and the data section (3 pages) in `thesis2/text/sections/`, every fact sourced to `data/facts/` or a document. Figure 1 and Table 1 contents listed for L.
- [ ] **Tue 27 to Fri 30 [L], data the replication needs:** (a) `thesis2/data/omxsb/tracker_aum.csv`, the yearly SEK assets of the OMXSB trackers 2013-2026, hand-built from the fund list and sources in `omxsb_notes.md` section 5 (fact sheets, annual reports); `replication_omxsb.py` reads it and it does not exist yet. (b) Appendix Table A1, the procurement calendar: every round with award, letter, execution dates, losers, redeemed share, money moved, destination, source per date, from `data/FTN/` and `data/measurements/bids_long.csv`. (c) Swing-pricing status for the 29 UNKNOWN rows in `thesis2/data/swing/swing_status_ftn_losers.csv` (mostly Luxembourg funds: prospectus or KID, "swing pricing" / "justerat fondandelsvärde"), with the source URL per row.
- [ ] **Tue 27 to Fri 30 [A], literature:** `thesis2/literature/cards.md`, one four-line card per paper to be cited (25 to 30 of the 66), starting with the anchor read twice; verify every [M] entry; novelty re-check for 2024-2026 work on Fondtorgsnämnden (Google Scholar cited-by on Greenwood and Sammon 2025; SSRN; DiVA for Swedish theses on fondtorget).
- [ ] **Thu 29 to Sun 1 [L]:** `replication_omxsb.py` to the end; Table 2 and Figure 2 as `.tex` and `.pdf` in `thesis2/output/`; one sentence in `output/tables/NOTES.md`. `pressure.py`, then `power.py --dose`. **Gate 3.**
- [ ] **Fri 30 [both]:** Friday swap (one afternoon). Three lines to Klug.

### Week 2 (2 to 8 Nov): sign-off and unblinding
- [ ] **[A]** Klug meeting with Table 2 in hand; minutes with the five decisions in `thesis2/03_DATA.md` E, dated. **Gate 4.**
- [ ] **[L]** Request the SHoF refresh (Valuations and Reinvestments to 31 Oct, same request as before).
- [ ] **[L]** After the sign-off commit: `ftn_eventstudy.py` for Table 3 and Figure 3 on the rounds with dated tranches (European 2024, Swedish active, Nordic active).
- [ ] **[A]** Theory section (3 pages, four equations, derivations cited); related literature (under one page); methodology (2.5 pages) from `01_DESIGN.md` 4 and 5.
- [ ] **[both]** Friday swap; three lines to Klug.

### Week 3 (9 to 15 Nov): all main results, data freeze
- [ ] **[L]** SHoF refresh in; `detect_exit_days.py` again; small-cap tranches added to the dose. Table 4 (anticipation), Table 5 and Figure 4 (incidence), Table 6 (cost-benefit) and Table 7 (robustness). One script per exhibit; `thesis2/code/run_all.sh`.
- [ ] **[A]** Results sections 6.1 to 6.5 from the NOTES sentences; introduction (3 pages, numbers previewed); conclusion last, calibrated with `research/reference/conclusions_winners_vs_nonwinners.md`.
- [ ] **Fri 13 Nov: data freeze. Gate 5.** Nothing new enters after this except FI 2026Q3 if it lands, as an appendix check.

### Week 4 (16 to 22 Nov): the draft
- [ ] **[L]** Clean-machine run from raw data; captions by the caption rule (equation, variables, sample, standard errors); appendix A1 to A3.
- [ ] **[A]** Abstract; related literature trimmed; references 25-30, each cross-checked; page count.
- [ ] **[both]** Mid-term meeting with Klug if his date falls here: bring Tables 2, 3 and 5, nothing else.
- [ ] **Fri 20 Nov: full draft to Klug. Gate 6.**

### Week 5 (23 to 29 Nov): attack the draft
- [ ] **[A]** Outside referee read (someone who has not seen the work lists unsupported claims); fix every one.
- [ ] **[L]** Number audit: every figure in the text traced to a script output; replication package (code, derived tables, data dictionary, README with run order, licensed inputs named, not shipped).
- [ ] **[A]** AI appendix from the log; format checklist (front page, no table of contents, 12 pt, single spacing).

### Week 6 (30 Nov to 6 Dec): finish
- [ ] Klug's comments in; second proofread on paper; replication zip tested from scratch.
- [ ] **Fri 4 Dec: submission-ready. Gate 7.** Submit **Mon 7 Dec, 10:00**: Canvas plus the zip to Anneli Sandbladh.
- [ ] Presentation and opposition before 12 Dec; Publish Thesis by 18 Dec, 18:00.
