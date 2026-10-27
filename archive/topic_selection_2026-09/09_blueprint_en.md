# Synopsis blueprint (skeleton to write from, in your own words)

**Header:** BE451 Thesis Synopsis, Fall 2026 · Students: name (ID), name (ID) · Preferred tutor: Alvin Chen

---

## Topic 1: [Title: e.g. "Do Taxes Depress or Stimulate Borrowing? Sweden's 2019 Corporate Tax Reform"]

**1. Research question** (1 sentence, italic)
- *Did Swedish private firms borrow less or more after the 2019 reform, and does the answer differ between firms that only got a lower rate and firms that lost interest deductions?*

**2. Motivation** (1 paragraph, 5–7 sentences)
- What the reform did: rate 22 → 21.4 % (2019) → 20.6 % (2021); deductions capped at 30 % of EBITDA; SEK 5 million always deductible per group.
- Why the two parts pull in opposite directions under standard theory.
- Why the US evidence (Ivanov et al.) contradicts standard theory.
- Why Sweden is a better test: all limited companies observed, a sharp threshold, both treatments in one law.
- One sentence: why a null result is still informative.

**3. Closest literature and contribution** (4 short paragraphs + 1 contribution paragraph)
- Ivanov, Pettit & Whited (2026, REStud): what they did, what they found, what we replicate.
- Sanati & Beyhaghi (2025, RFS): threshold design at USD 25m; what we replicate at SEK 5m.
- Heider & Ljungqvist (2015, JFE): the elasticity we use as benchmark.
- Brok (2026, JFQA; 2024, RoF): why the threshold must be computed per group.
- "Relative to … we … Our contribution is threefold: first … second … third …"

**4. Data and feasibility** (1 paragraph or bullets)
- Serrano: all Swedish limited companies 2013–2024; variables: debt, interest expense, tax expense, EBITDA, investment, group parent.
- Access: verified on [date] via SWAMID; N ≈ [number].
- Main risk + fallback (e.g. group aggregation infeasible → firm-level threshold with caveat).

**5. Empirical method** (1 paragraph or bullets)
- Test A (rate cut): difference-in-differences, high vs low pre-reform tax exposure, before/after 2019 and 2021; firm and industry×year fixed effects.
- Test B (cap): bunching at the SEK 5m kink in group net interest (kink, not discontinuity); bound vs unbound by the 30 % rule.
- Outcomes: leverage, new borrowing, interest/debt, investment.
- Threats and how handled: 2022 rate hikes (industry×year FE); intra-group shifting (group aggregation); manipulation at threshold (bunching is itself a finding).

**6. Three-month plan** (3 bullets)
- MVP: Test A. Extension: Test B + group channel. First data test this week: Serrano variable list.

**References** (syllabus format, alphabetical) — copy from `03e_synopsis_topic_I.md`.

---

## Topic 2: [Title: e.g. "What Does the Threat of a Profit Cap Cost? Political Uncertainty and Sweden's Private Welfare Firms"]

**1. Research question** (1 sentence, italic)
- *How did private welfare firms respond to the threat of a statutory profit cap in 2016–2018, in investment, payouts and ownership changes, and did the response reverse when the Riksdag rejected it?*

**2. Motivation** (1 paragraph)
- The timeline: inquiry 8 Nov 2016 → bill 19 Mar 2018 → rejected 7 Jun 2018 → renewed threat 2022, bill 25 Jun 2026, election 13 Sep 2026.
- Who was affected: private schools, care, personal assistance; many PE-owned.
- Two mechanisms with opposite implications: wait-and-see (investment down) vs cash-out-now (payouts up).
- Why a null is informative (the threat was never credible).

**3. Closest literature and contribution**
- Julio & Yook (2012, JF): election-year investment drop of 4.8 %; what we replicate; what we change (sector threat instead of elections).
- Jens (2017, JFE): causal evidence + placebo logic; our placebo = private health care (SNI 86), excluded from the bill.
- Kelly, Pástor & Veronesi (2016, JF): theory behind the payout prediction; small event study on Attendo, Humana, AcadeMedia, Ambea.
- Bonaime, Gulen & Ion (2018, JFE): policy uncertainty and M&A; ownership changes as third outcome.
- "Relative to … we … Our contribution is threefold: …"

**4. Data and feasibility**
- Serrano 2012–2024; treated: SNI 85, 87–88; placebo: SNI 86; controls: matched private service firms.
- Access verified on [date]; N ≈ [number] treated firms.
- Risks + fallback: 2019 owner-screening rule (keep main window 2016–2018); small listed sample (event study illustrative only).

**5. Empirical method**
- Difference-in-differences around the three 2016–2018 dates; firm and industry×year fixed effects.
- Outcomes: investment/assets, dividends, group contributions, employment, exit, ownership change.
- Mechanism splits: PE-owned vs other; profits above vs below the proposed cap.
- Robustness: SNI 86 placebo, pre-2016 pseudo-events, exclude asylum housing (SNI 87.9).

**6. Three-month plan**
- MVP: 2014–2020 DiD with placebo. Extension: 2022–2026 episode, PE mechanism, event study.

**References** — copy from `03c_synopsis_draft_H_G.md`, Topic 1.

---

**Format check:** 1–2 pages per topic, 12 pt, single spacing, English, PDF named `BScThesis_Surname1_Surname2.pdf`, submitted in Canvas before 9 Sep 13.00. Every cited paper appears in the reference list and vice versa. Log AI use (tools, dates, purpose).
