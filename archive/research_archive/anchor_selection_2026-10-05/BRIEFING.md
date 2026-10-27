# Shared briefing for the final anchor decision (read fully before working)

You are one of several agents deciding the ANCHOR PAPER for a BSc finance thesis. Other agents will attack your output, so every factual claim must be verifiable: cite page, table or line for papers; file, column and code for data. Never invent a number. Write "not verified" where you could not confirm something. Quality over speed.

## 1. The thesis setting

- Two SSE students (BE451 Degree Project in Finance, Fall 2026). Submission 7 December 2026 (about nine weeks from 4 October). Final version 18 December.
- Topic: Sweden's Fondtorgsnämnden (FTN), created 2022. Since 2024 it procures the premium pension (PPM) fund platform one category at a time. Funds bid (score: quality 75%, cost 25%), a few win, losing and non-bidding funds are removed from the platform, and the PPM capital of savers in removed funds is moved by default to winners unless the saver actively chooses (reported default acceptance 85 to 95%). Procured fees fall sharply.
- Award dates and admission months (Pensionsmyndigheten; admission is not the same as the verified transfer date): Europe active, award 25 Mar 2024, admitted June 2024; Europe index and global index, award 31 Oct 2024, admitted Feb and Mar 2025; Nordic large/mid and Nordic small cap, award 19 Feb 2025, admitted Apr 2025; Sweden active and Sweden passive, award 27 Aug 2025, admitted Dec 2025 and Oct 2025; global active, award 24 Feb 2026, under appeal; Europe small cap and Sweden small cap, award 28 May 2026, admitted Jul and Aug 2026; global technology, award 22 Sep 2026.
- Older events: a 2019 tightening of platform rules (prop. 2017/18:247) removed several hundred funds, and non-choosers' capital went to the default fund AP7 Såfa. Each December, new contributions are placed into savers' existing choices.
- Tutor: Michael Klug (SSE PhD 2023, "Essays on Index Investment": index inclusions, front-running around Russell reconstitutions, price elasticities around IPO inclusions, ML prediction of inclusions; interests also include performance measurement of mutual funds). His topic prompt: "Effects of Fondtorgsnämnden since 2022 on fund supply, quality, fees, investor behaviour or market efficiency. Main risk: short post-period and exact policy/selection design."
- Examiner (grades the thesis): Riccardo Sabbatucci (SSE; JF 2020, RFS 2020, RoF 2025; working paper with Tamoni and Xiao, "Shifting From Active to Passive: How Retirement Plans Impact Equity Prices", April 2026).
- Course rules: read /mnt/user-data/uploads/financethesis_ny/tmp/pdfs/course_intro.txt and syllabus.txt. Key quotes: "Standard for BSc thesis: replication and extension of a (recent) published paper in a top journal ... The extension needs to be meaningful. Avoid default option of applying the question to Nordic countries unless meaningful." "A robust research question is a question that is interesting independently of the results." "Do not chase statistical significance." "Minimum detectable effect: check the power of your test." "Simpler is better!"
- Submitted synopsis: /mnt/user-data/uploads/financethesis_ny/tmp/pdfs/synopsis.txt. It promised fees on and off platform, fund supply (removed funds shrink, close, merge), saver active choice versus default, and whether funds perform worse after large inflows.

## 2. Evidence on what wins (from earlier audits; verify, do not just repeat)

Sources:
- Full texts of 25 awarded theses: /home/claude/uvangludvig-ship-it/financethesis/old_winners/text/ (index: old_winners/INDEX.md).
- 635 others: non_winners/text/<MediumId>.txt (index: non_winners/INDEX.md).
- Earlier AI analyses: /tmp/claude-0/-home-claude/fccbaf89-b6ff-5381-beaa-3003648c0fd8/scratchpad/anchor_final/prior_analyses/ (winners_vs_nonwinners_analysis.md; conclusions_winners_vs_nonwinners.md; a rival review in WINNERS_AND_EXAMINER.md and RECOMMENDATION.md).

Earlier claims, to be tested:
1. 15 of 25 winners have an anchor whose question equals the thesis question.
2. 9 of 25 are table-level replications, all from 2016 onward; 7 of 12 since 2019.
3. Six winners exploit a reform with a dated treatment and a control; none of 33 sampled non-winners do.
4. The extension sits inside the anchor's tables.
5. Winners compare their numbers to the anchor's.
6. Winners' conclusions are calibrated to their tables (over-claiming: 16% of winners, 58% of non-winners).

The rival review warns:
- the "non-winner" label is imperfect (6338 was later awarded);
- the old metrics script was unsafe (a "DiD" regex also matched "did");
- 4441 (pre-FOMC drift) had an anchor and an updated sample but did not win;
- strong non-winners exist (5880, 2324);
- several recent winners name Adrien d'Avernas, not Sabbatucci, as examiner.

## 3. Data that actually exist (verified 4 Oct 2026 unless marked otherwise)

- **Pensionsmyndigheten monthly fund files, Jan 2001 to Aug 2026.** 308 files in /home/claude/uvangludvig-ship-it/financethesis/data/raw/<period>/<year>/. The 128 old .xls files are already converted to .xlsx in /tmp/claude-0/-home-claude/fccbaf89-b6ff-5381-beaa-3003648c0fd8/scratchpad/xls_conv/. A format survey from an earlier agent is in scratchpad/audit/survey.json and survey_changes.txt.
  - Recent sheet "Fondval & marknadsvärde": Fondnummer, Fondnamn, savers (women, men, total), PPM market value (women, men, total), "Handel, netto", category, type, manager, Aktiv/Passiv, Svensk/Utländsk, "Upphandlad" flag.
  - Sheet "Fondstatistik": returns, fees net and gross, ISIN. Locate columns by header text; positions change across vintages.
  - The scope of "Handel, netto" is not defined in the files. Verify before relying on it.
- **Parsed panel for Jun 2023 to Aug 2026:** scratchpad/audit/pa_panel_2023_2026.csv (columns date, fid, name, savers, mv, nt, cat, typ, mgr, ap, sf, proc, isin). In some older-format rows, ap and sf are shifted.
- **FTN winners' inflows (scratchpad/audit/winner_doses.csv).** 21 active winners so far, 14 with more than SEK 50m inflow.
  - Inflow divided by total fund AUM (Morningstar snapshot of Jan 2026, SEK funds, n=17): median 6%, p75 11%, p90 23%. Only two are at or above 20% (Cliens Sverige 33%; Simplicity Sverige, AUM SEK 278m).
  - Median 7 post-transfer months, max 17.
  - The Sweden small-cap transfers had not happened by Aug 2026.
  - Removed equity funds are visible by month: about 65 in procured categories, plus about 35 winners so far.
- **FTN procurement reports (all 11), text extracted:** scratchpad/ftn_txt/*.txt (PDFs in /mnt/user-data/uploads/financethesis_ny/data/FTN/). They list submissions, qualification, interviews, winners with ISIN and procured fee, fees before and after, capital and savers. Example: the first Europe report has 35 submissions, 23 fail initial requirements, then one withdrawal and one exclusion at the interview threshold, leaving 10 fully evaluated funds and 6 winners.
- **SHoF Morningstar (licensed), daily data aggregated to monthly:**
  - /mnt/user-data/uploads/financethesis_ny/tmp/anchor_final/shof_valuations_monthly.csv: performanceId, ym, secid, ccy_class, ccy_fund, last_date, tnaclass, tnafund, nf_class, nf_fund (sum of daily estimated net flows), ndays, nf_class_n.
  - shof_rips_monthly.csv: performanceId, returntype, ym, last_date, tri_sek (month-end reinvested-price index in SEK; returntype 1 for all ids, 18 for some).
  - Coverage 2018-01 to 2026-09, 4,984 performance ids. All 482 PPM funds with an ISIN in the 2023 to 2026 files are covered.
  - CAUTION: Swedish-domiciled funds report a nonzero net flow in only 32% of fund-months and daily observations in 29% (Luxembourg funds: 90% and 86%). A zero "netflow" is often missing, not zero. For Swedish funds, impute flows from TNA and returns: flow_t = TNA_t − TNA_{t−1}(1+R_t).
  - tnafund repeats across share classes; do not sum it.
  - Example: AMF Aktiefond Europa (ISIN SE0000739153, performanceid 0P00000K17) has monthly TNA only, with net flows recorded as 0. TNA rose from SEK 9.82bn (Feb 2025) to 11.19bn (Mar 2025) when PPM showed a SEK 1.39bn inflow.
  - Field definitions: /mnt/user-data/uploads/financethesis_ny/research/anchor_review/sources/shof_field_definitions.txt.
  - Pre-2018 SHoF history was not downloaded. SHoF says it holds older history.
- **Morningstar fund master:** scratchpad/audit/fundmaster.pkl (80,258 share classes). obsoletetype is blank for all 10,437 obsolete classes, and no field links a merged fund to its acquirer.
- **Morningstar fee file:** scratchpad/audit/fees.pkl (FEES.txt; prospectus-date fee snapshots).
- **Finansinspektionen quarterly fund holdings (Swedish-domiciled funds only):** zips for 2023Q4, 2024Q1, 2024Q2 and 2026Q2 in /mnt/user-data/uploads/financethesis_ny/research/anchor_review/sources/. Other quarters are public at fi.se but not downloaded; the container's shell usually cannot reach fi.se.
- **Other files in the same sources folder:** Pensionsmyndigheten daily NAV workbook for 2024 (ppm_nav_2024.xlsx); the Cookson et al. accepted manuscript (cookson_et_al_accepted_2019.txt/.pdf); Cooper, Halling and Yang (2021) text.
- **Sialm, Starks and Zhang (2015) full text:** /tmp/claude-0/-home-claude/fccbaf89-b6ff-5381-beaa-3003648c0fd8/scratchpad/ssz.txt (pdftotext of the JSTOR PDF; rotated tables are garbled). The PDF is /root/.claude/uploads/fccbaf89-b6ff-5381-beaa-3003648c0fd8/de6cc45a-Sialm_et_al._-_2015_-_Defined_Contribution_Pension_Plans_Sticky_or_Discerning_Money.pdf. Use Read with pages to view tables as images: Table III p.16, Table VIII p.27, Table IX p.30.
- **WRDS (CRSP, Thomson) is available via SSE:** not verified for this group.

## 4. Candidates so far

**(A) Sialm, Starks and Zhang (2015 JF), reframed.** Question: what happens when a sponsor is introduced into a participant-only pension system?
- Replicate Tables II, III and IX on PPM (participants only) before 2024.
- Extend Table VIII with an FTN "sponsor flow" column (removed funds −100%; winners' transfer inflows).

**(B) Cookson, Jenkinson, Jones and Martinez (2021 RFS), "Best Buys and Own Brands".** Question: does FTN selection move money outside PPM, and what does it select on?
- Rival review's first choice.
- Earlier power analysis: outside-PPM flow DiD has 8 to 12% power; the selection logit is powered.

**(C) Da, Larrain, Sialm and Tessada (2018 RFS), "Destabilizing Financial Advice".** Question: stock-level price pressure from FTN transfers.
- Earlier concerns: netting within category (never computed); three events; no replication independent of FTN; drift from Klug's prompt; fragile holdings data.

Rejected so far, and why:
- McLemore (2019 JFQA) plus FTN as size shocks: doses too small; mergers not identifiable.
- Pool, Sialm and Stefanescu (2016) plus Pástor, Stambaugh and Taylor (2015) hybrid: PSS has no DiD; PST's fund-level effect is insignificant and the paper has no Active Share; the design asks two questions.
- December-placement price pressure: unverified.

## 5. Output rules

- Write your full report in markdown to the file path you are given, then return the same report as your final message.
- Separate VERIFIED facts (with source) from JUDGEMENTS.
- For every risk you identify, give a concrete solution or mitigation, and say whether it fully solves or only reduces the risk.
