# Revision blueprint: Sabbatucci's course requirements and prior winners

Prepared 12 November 2026. Read-only review of the supplied course originals, the source texts of four prior winners, and the current draft. This is an editorial blueprint, not an assessment of likely grades or prize outcomes.

## 1. Evidence and the distinction that matters

The controlling evidence for Riccardo Sabbatucci's preferences is his **Fall 2026 course syllabus and introductory lecture**, not previous students' papers. The title pages of the 2021 microstructure, 2023 FOMC and 2024 French-quota papers identify **Adrien d'Avernas** as examiner. They therefore cannot establish Sabbatucci's individual assessment preferences. They can demonstrate successful ways to organize an empirical paper.

The original PDFs read are:

- `tmp/thesis_draft_20261112/source/reference/course_context/source_materials/Syllabus_Fall_2026.pdf` (10 PDF pages, version 14 August 2026).
- `tmp/thesis_draft_20261112/source/reference/course_context/source_materials/Introduction_to_research_in_finance_Fall_2026_RS.pdf` (27 slides).
- Fresh text extractions are saved beside this report as `syllabus_verified.txt` and `course_intro_verified.txt`.

The local source notes identify the authenticated Canvas course as `https://sse.instructure.com/courses/2864`, syllabus item `92597`, and introductory lecture item `92598`. I checked the downloaded PDFs, not the current live Canvas state. Those source notes record retrieval on 3 September 2026; no new assertion about a subsequent course update is made here.

Prior winner evidence was read from the actual full-text extractions, including introductions, methodology, main results, discussion and conclusions, rather than relying on the existing winners-analysis summaries. Page references below refer to **printed page numbers**, unless explicitly stated otherwise.

## 2. What Sabbatucci explicitly asks for

| Requirement | Original location | Consequence for the revision |
|---|---|---|
| A useful, correct, relevant and meaningful contribution; independent work | Intro slide 4 | Explain what the Swedish evidence adds to the anchor paper. A long list of successful code checks is not the economic contribution. |
| Do not chase statistical significance; study the question and possible channels | Slide 5 | Keep imprecise results where relevant. Do not reorganize around whichever extension happens to be significant. |
| Standard approach: replication and meaningful extension of a recent top-journal paper | Slide 10; syllabus p. 4 | Make Greenwood and Sammon the organizing paper. State exactly which exercises are reproduced and which are adapted or added. |
| A Nordic setting alone is not automatically a meaningful extension | Slide 10 | Motivate differences in benchmark construction, investors/holdings measurement and event timing. Do not claim these differences explain results without testing that link. |
| Simpler methods are preferable; complexity requires justification | Slide 13 | Remove the invented illustrative lambda decomposition. A replication does not need an additional structural model that is neither estimated nor tested. |
| Start from the nearest literature's quantitative exercise | Slide 17 | The reader should see the core replication result before advanced auxiliary inference or peripheral diagnostics. |
| No student-project digressions or pedagogical explanations of standard methods | Slide 18 | Remove repeated audit/provenance narration, textbook OLS explanations, lists of alternative methods and internal process labels from the main text. |
| Introduction 2–4 pages: motivation, question, methodology, results, interpretation | Slide 19 | A reader stopping after the introduction should know the question, headline estimates, meaningful extension and calibrated answer. |
| Related literature under one page | Slide 19 | Focus on Greenwood–Sammon and the few closest comparisons; avoid a broad literature survey. |
| Data and Methodology → Main Empirical Analysis → Interpretation/Discussion → Conclusion | Slide 19 | Use this directly as the high-level spine. |
| State/consider statistical power | Slide 20 | Explain what the final-period interval can and cannot resolve. A full MDE derivation need not be in the main text. |
| Mandatory official cover; Journal of Finance style; no table of contents | Syllabus p. 5 | Preserve formal requirements. Earlier winners are not controlling when their formatting differs. |
| Maximum 40 single-spaced 12pt pages excluding appendix; main text approximately 25–40 pages including relevant exhibits | Syllabus pp. 5–6 | Aim for roughly 25–30 substantive main pages. Do not pad to mimic the longest winner or compress to a 17-page historical example. |
| Simple, transparent, direct writing is a quality criterion in its own right | Syllabus p. 6 | Every paragraph should deliver a finding, explain a necessary choice, or connect evidence to the research question. |
| Important exhibits in the main text; supplementary exhibits after references; captions self-contained | Syllabus p. 6 | Keep a small, coherent core of tables and event-time figures. Move secondary comparison/twin/OMXS30 checks to appendices. |
| Extended mathematical derivations that are not the contribution belong in self-contained appendices | Syllabus p. 6 | Move Fieller calculations, bootstrap inversion, dependence-estimator details, multiplicity mechanics and MDE algebra out of the main text. |
| Cite sources influencing topic, format, methods and writing; do not copy uncredited prior theses | Syllabus p. 4; slide 25 | Retain an accurate acknowledgement of structural benchmarks. Do not reuse their prose or imply their results support this thesis's economic claims. |

The syllabus also contains the already disclosed AI-writing restriction on p. 10. It does not alter the structural recommendation: a clear research working draft remains the appropriate status of this AI-produced artifact.

## 3. What the winners actually do

### Holst and von der Esch (2023): *Changing Patterns over the FOMC Cycle*

Official PDF: https://arc.hhs.se/download.aspx?MediumId=5734

Actual order and page allocation:

| Section | Printed pages | Function |
|---|---|---|
| I. Introduction | 2–4 | Introduces Cieslak, Morse and Vissing-Jorgensen, motivates the later sample using concrete changes, asks whether the even-week pattern persists, then states numerical results and the mechanism argument. |
| II. Theoretical Framework | 5 | A focused one-page comparison to the anchor and alternative risk explanations; three explicit contribution dimensions. |
| III. Data Description and Methodology | 6–9 | Starts by promising the closest possible data comparability to the original; organizes datasets by the economic purpose they serve. |
| IV. Analysis and Results | 10–16 | Plots the return pattern first; reproduces original-period results beside later-period results; only then examines changes in meeting timing and monetary policy. |
| V. Discussion | 17–20 | Adds the VIX-based implication of competing explanations and returns to the original question. |
| VI. Conclusion | 21 | Answers the persistence question and the mechanism question. |
| References; appendices | 22–27 | Narrative extracts, dates, frequency and supplementary evidence. |

Main-text span: **20 printed pages**, not 25. This old length does not override current guidance.

The main craft lesson is the chain: **anchor result → reason the new sample is informative → same quantitative exercise → direct comparison → selected mechanism evidence**. The main figure is a return-path figure, not a collection of diagnostics. The regressions are introduced when they answer the next economic question. Technical methods are not the paper's declared contribution.

Do not imitate its stronger causal rhetoric mechanically. Its own observational mechanism comparisons do not entitle this thesis to use causal claims.

### Fager and Öhman Tunklint (2024): *The Smooth Transition*

Official PDF: https://arc.hhs.se/download.aspx?MediumId=6053

| Section | Printed pages | Function |
|---|---|---|
| 1. Introduction, including run-in related literature | 2–4 | Names Ahern and Dittmar in the first paragraph, asks the research question, explains France versus Norway, describes short- and long-term replication exercises, reports results and possible institutional explanation. |
| 2. Data and Methodology | 4–11 | Data gathering; summary statistics; institutional setting; event study; long-term specification. |
| 3. Results | 11–15 | Event study first, longer-term firm value second, board characteristics as the mechanism evidence. |
| 4. Discussion | 15–18 | Compares its estimates to the anchor's estimates, then discusses whether longer adjustment and different sanctions fit the findings. |
| 5. Conclusion | 18 | Concise answer and contribution. |
| Appendices; references | 19–27 | Supplementary regressions and AI disclosure; references are last in this particular older paper. |

Main-text span: **17 printed pages**. Its appendix-before-references order conflicts with current course instructions and should not be copied.

The useful lesson is not that a null result is enough. It is the direct relationship between **each replicated test, the published comparison, and the institutional difference that makes the extension worth doing**. The paper has three numbered formulas (a variable definition and empirical specifications), not an invented formal decomposition of all possible mechanisms.

Some claims turn insignificant estimates into assertions of no adverse effect. Retain this draft's more disciplined distinction between imprecision and evidence of economic absence.

### Domeij and Krieg (2021): *Market Microstructure Invariance, Bid-Ask Spreads and Impact Costs in the Swedish Stock Market*

Official PDF: https://arc.hhs.se/download.aspx?MediumId=5028

| Section | Printed pages | Function |
|---|---|---|
| Introduction | 2–4 | Two precise research questions and the reason high-frequency Swedish data extend the theory. |
| 1. Fundamental Concepts | 5–6 | Terminology. |
| 2. Literature Review | 7–8 | Three model papers and what is taken from each. |
| 3. Theoretical Background | 9–17 | The equations generate the proportionality prediction and price-impact model actually tested. |
| 4. Hypotheses and Research Design | 18–22 | Explicit quantitative hypotheses and estimation. |
| 5. Data | 23–29 | Data by research question, limitations, construction and summary statistics. |
| 6. Empirical Findings | 30–37 | Spread–illiquidity relation first; crash-model application second. |
| 7. Concluding Remarks | 38–39 | Answers each question, limits model validation and explicitly disclaims causal conclusions. |
| References; appendices | 40–45 | Supplementary regressions and construction details. |

Main-text span: **38 printed pages**. It is not an appropriate template for adding theory to an event-study replication: its many equations matter because its principal exercise tests a mathematical model. The current thesis does not estimate the added lambda decomposition.

The same paper explicitly states on p. 39 that its regression evidence does not permit causal conclusions. A causal design is therefore not necessary to resemble a previous winner; a clear, well-executed question is. Its glossary and general-method explanation are also at odds with Sabbatucci's current slide 18.

### Barketorp Dirke and Ye (2016): *Intermediary Asset Pricing and the Swedish Equity Market*

Official PDF: https://arc.hhs.se/download.aspx?MediumId=2854

This is an especially useful comparator because it is an explicit Swedish adaptation of recent major papers.

| Section | Printed pages | Function |
|---|---|---|
| I. Introduction | 1–2 | Names both anchor papers, explains their competing economic frameworks, states the quantitative method and benchmark comparison, gives numerical results. |
| II. Research question | 2 | A very short explicit statement. |
| III. Theory and Previous Literature | 2–5 | Explains why the theories differ and why Swedish intermediary data matter. |
| IV. Data | 5–13 | Documents the difficult original Swedish factor construction and matched comparison samples. |
| V. Empirical Approach | 14–15 | The actual two-pass regressions, performance measure and inference. |
| VI. Empirical Results | 15–21, with exhibits continuing through 23 | The main pricing table comes first; the interpretation compares models on matched samples. |
| VII. Discussion and Further Research | 21–24, interrupted by exhibits | Confronts data limits and what alternative methods could add. |
| VIII. Conclusion | 24–25 | Reports the benchmark-relative result without claiming the preferred model is universally true. |
| References; appendices | 26–38 | Further measurement and robustness. |

Main-text span: **25 printed pages**. The argument distinguishes **better than a comparator** from **correct in an absolute sense**. The paper also explicitly says on p. 24 that its purpose is a Swedish out-of-country test, not econometric elaboration for its own sake. This is the closest lesson for the current rewrite: the anchor exercise and Swedish measurement should be central; statistical machinery should serve them.

## 4. A concrete replacement architecture

Use the 2023 paper's sequence of argument, the 2024 paper's compactness, and the 2016 paper's explicit mapping from anchor model to Swedish implementation. Let the verified Greenwood–Sammon paper control the **economic sequence of tests and definitions**. Do not infer exact original windows, multipliers or table numbers from this structural review; those require the separate anchor-paper due diligence.

### 1. Introduction — about 3–4 pages

1. Begin with Greenwood and Sammon's economic puzzle and the particular original finding being examined.
2. Explain in concrete terms why the Swedish setting tests something meaningful beyond geographic transfer: benchmark membership rules, scheduled review timing, and the ability to connect returns to reported benchmark-linked holdings. State measurement limitations briefly, without claiming these setting differences cause the outcome.
3. State one primary question: whether the changing return pattern documented in the anchor is also present around OMXSB reconstitutions. A connected second question asks how the return pattern relates to measured benchmark-linked trading. Do not create a separate hypothesis for every available dataset.
4. State the sample, primary return window and replication/adaptation in one paragraph.
5. Report two or three key numerical answers. The four-period return sequence and its uncertainty; the later-decade addition result; holdings/trading evidence in the exact scope the anchor comparison supports.
6. State the contribution as economic evidence in a different institutional and measurement setting, not as a collection of restrictions on inference.
7. Give one paragraph on scope and causal interpretation, then a short roadmap.

Do not begin with general observations about how all index events are endogenous. Do not call the paper's contribution an “empirical boundary”. The reader should be able to explain the result after these pages.

### 2. Related literature — under one page

Greenwood–Sammon first and longest. Include only the nearest studies required to explain the question, the price-pressure interpretation, or the holdings measure. State how the current exercise differs. A methods bibliography is not the economic literature section.

### 3. Data and methodology — about 6–7 pages, including exhibits

Suggested subsections:

- **OMXSB reconstitutions:** the event and its announcement/effective timing; why the rules matter for comparison with the anchor. One simple timeline if helpful.
- **Sample and sources:** event inventory, exclusions, return sample, holdings sample, sample counts by period. Show the main sample construction once.
- **Replicating Greenwood and Sammon in Sweden:** a concise implementation table covering index, sample, returns/windows, holdings measurement, composition adjustment, and inference. Clearly mark what is the same and what is adapted.
- **Return and holdings measures:** only equations needed to reproduce the reported quantities; define every symbol immediately. Explain the ratio in ordinary economic units.
- **Estimation and uncertainty:** a short paragraph on review clustering and the actual interval method, why simultaneous changes matter, and where sensitivity details are reported. No textbook OLS or bootstrap lesson.

The sample and methodology should prepare the reader to understand the first result table. Do not make the reader traverse a new structural model before seeing the replication.

### 4. Empirical results — about 9–10 pages, including exhibits

Recommended sequence, to be aligned with the verified anchor paper:

1. **How have returns around index changes evolved?** Main replication table with announcement, implementation and total-window returns; period counts and consistent units. Explain additions and deletions. Then direct contrasts, rather than differences in significance.
2. **Where in the event do returns occur?** One coherent cumulative-return figure on a fixed sample, with event timing clear. Discuss pre-announcement, announcement-to-implementation and post-implementation timing only to the extent the data actually support it. Do not splice differently selected cohorts or normalize away relevant differences.
3. **Does observable composition account for the pattern?** The anchor's composition exercise, same-sample comparison and necessary timing checks. Use a compact table; the invalid overlap must be repaired or the result demoted.
4. **What does measured benchmark-linked trading show?** Holdings and the return-to-demand ratio if genuinely part of the anchor; place the economic interpretation first. Keep denominator uncertainty visible, but put the Fieller derivation in the appendix. Explain limited coverage directly.
5. **How robust is the main return result?** A small set of pre-existing economically motivated exclusions, the main quantitative sensitivity and any clear qualification. Report them as separate checks, not as a search for significance.

Volume concentration and quoted spreads belong with the relevant anchor mechanism comparison. If they do not distinguish explanations, treat them as descriptive context and avoid a full parallel story.

### 5. Discussion — about 3–4 pages

Answer in order:

- Which Greenwood–Sammon finding is reproduced, which differs, and which cannot be compared cleanly?
- What do the joint return/holdings/trading facts contribute economically?
- Which explanations are consistent with them, and which claims are beyond the design?
- What does the fixed-cohort ED+20 extension add, if it is retained? Label it as exploratory and make clear that it does not establish permanent impact. It should deepen the core question, not displace the replication as the headline.
- Which remaining limitations materially alter the answer? Collect the repeated caveats in a concise, specific subsection.

Avoid repeating the entire results section or the code audit. No claim of liquidity improvements causing attenuation unless supported by an identified design.

### 6. Conclusion — about half to one page

Answer the introduction's question in the same terms; give the key magnitude; explain the incremental knowledge; state the one most important unresolved boundary. Do not conclude merely that “more research is needed”. Do not announce that an effect has disappeared because a p-value exceeds 0.05.

The allocation is approximately 25–30 main pages with normal exhibit flow. It is a substantive target, not a requirement to fill space.

## 5. Equations and material to remove or relocate

| Current material | Recommended treatment | Why |
|---|---|---|
| `CAR_i = lambda_i Q_i + I_i + B_i + U_i` | **Remove**, not merely rename | It is explicitly an unestimated interpretive device added by the assistant. It makes the study appear to develop a model it does not use. Explain confounding in plain sentences. |
| `D_obs = kappa Q + eta` | **Remove** | State that coverage changes can change measured holdings without an equal change in total index demand. The notation adds no empirical result. |
| Exact market-adjusted CAR definition | **Keep** | This defines the main reported variable and makes arithmetic versus compounding explicit. Use the actual verified replication convention. |
| Holdings-change and return-to-demand ratio | **Keep if central to the anchor exercise** | Essential to interpret the units and numerator/denominator; explain a typical value verbally. |
| Full Fieller inequality, bootstrap inversion, jackknife/two-way formulas | **Appendix** | Valuable inference checks; not the economic research question or central replication specification. |
| MDE formula and equivalence-test mechanics | **Appendix** | Main text needs only the interval and clear statement of what the sample can resolve; the chosen margin and exploratory status must remain disclosed. |
| Non-overlapping cohort identity | Usually **prose**, with formal construction in appendix | The fixed-sample horizon idea can be explained simply. |
| “Inherited”, “audit”, “repository” throughout main narrative | **Rewrite around data, estimates and specification** | These are implementation/provenance terms. The research paper should read as the authors' coherent study, with provenance preserved in replication materials. |
| Twins, OMXS30, issuance, large collections of dependence diagnostics | **Appendix unless an essential anchor exercise** | Retain access without turning the main argument into a catalogue. Do not hide adverse evidence that changes a headline conclusion. |

## 6. Release gate for the revised draft

Before calling the revision clearer and more faithful, check:

1. The abstract and first three introduction pages answer the same question with the same main numbers.
2. Every main table or figure has a role in answering that question or adjudicating a specific explanation.
3. The anchor-paper implementation map is factually verified, including deviations; the label “replication” is scoped accurately.
4. The main text contains no unestimated lambda/coverage model and no advanced inference derivation.
5. The strongest result is presented before qualifications, but each material qualification is placed close enough that it cannot be missed.
6. Imprecision is not rewritten as absence; observational returns are not relabeled causal impact.
7. Course slide 19's section order, introduction/literature lengths, 12pt/single-spacing/page constraints and appendix placement are met.
8. The revised PDF is visually inspected, not merely compiled successfully.

A prize outcome cannot be established by matching headings. The useful transfer from these winners is their discipline: a named anchor, a motivated extension, the central exercise first, a small number of interpretable results, and a conclusion that answers the starting question.
