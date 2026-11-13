# The Index Effect in Sweden

Complete English working draft of **The Index Effect in Sweden: A Replication and Extension of Greenwood and Sammon (2025)**, with computational checks and reproducibility materials. Revised on 12 November 2026 for Alexander Fox and Ludvig Pauli Uväng.

Read the final [Word draft](final/The_Index_Effect_in_Sweden.docx) or its [matching PDF](final/The_Index_Effect_in_Sweden.pdf), then the [verification report](audit/verification_report.md). The [criteria audit](audit/criteria_audit.md) and [supplied-draft claim audit](audit/claude_claim_audit.md) document the final narrative revision. Editable section source starts at [main.tex](manuscript/main.tex); [its LaTeX rendering](manuscript/main.pdf) contains the same content with different pagination. The draft separates descriptive return associations from causal effects and labels all new analyses as exploratory.

**Submission status:** this is an AI-generated research draft. The BE451 Autumn 2026 syllabus permits disclosed AI assistance but prohibits AI directly writing thesis text. The authors must write the submitted text and verify the argument and sources. The PDF contains a full disclosure. This package does not represent a submission-ready or independently certified thesis.

## What the evidence supports

- Addition CAR falls from 8.52% in 2007–2011 to 1.50% in 2022–2026, without a monotonic decline. The 2017–2026 mean is 2.15%, with a 95% interval of [1.01%, 3.39%].
- The announcement-to-implementation interval also changes: its median is fourteen trading days in the earliest complete addition sample and six in the latest. On the same event cohorts, the initial seven-day returns are 1.19% and 1.80%. Their difference is imprecise; the full-window decline is concentrated in the remaining interval. This exploratory accounting does not identify a causal calendar effect.
- Reported benchmark-linked fund purchases and concentrated pre-implementation trading document activity. Changing holdings coverage and a restrictive share-adjustment screen limit historical demand-ratio comparisons.
- Fixed-cohort returns through ED+20 and within-firm share-class comparisons refine interpretation. Neither establishes permanent or causal price impact. A comparison-control timing overlap has been corrected; later addition results remain positive in that secondary descriptive comparison.

## Final narrative revision

The main text now follows the course's six-part sequence: introduction, concise related literature, data and methodology, empirical results, discussion and conclusion. Greenwood–Sammon supplies the empirical backbone. The unestimated lambda decomposition from the earlier draft has been removed. Three main equations define the measured return, the actual composition regression and the anchor's demand ratio; technical inference is in the appendix.

The final narrative asks whether the disappearing effect travels to Sweden and what remains. All empirical extensions appear in Results, followed by a discussion that connects the findings. The verified fund-flow table shows 1.03% mean purchases by covered OMXSB-linked funds, 0.40% by other observed passive funds and 1.19% by all included funds on the same 136 later additions. Unsupported cross-country multiplier comparisons, universal migration claims and causal bounds from sister shares are omitted.

The revision adds a version-specific [replication map](sources/greenwood_sammon_replication_map.md), a [course and winner comparison](sources/course_winner_blueprint.md), and an [empirical revision report](audit/replication_revision_report.md). Source manuscripts are distinguished from the published abstract; implementation equivalence to unavailable US code is not claimed. The original empirical source and primary outcomes are retained alongside clearly labeled retrospective checks.

## Find the supporting material

| Location | Contents |
|---|---|
| `final/` | Final editable Word draft and matching PDF |
| `manuscript/` | Shared text, bibliography, generated tables, figures and LaTeX rendering |
| `audit/verification_report.md` | Completed checks, discrepancies and unresolved issues |
| `audit/results/` | Return, timing, holdings coverage, repaired comparisons, dependence, horizon, ratio, multiplicity and equivalence calculations |
| `audit/analysis_addendum.md` | Dated exploratory specification and subsequent changes |
| `audit/exhibit_map.csv` | Exhibit-to-input map |
| `sources/` | Reference ledger, notice retrieval outcomes, data dictionary and structure benchmark |
| `replication/thesis_final/` | Frozen original code, declarations, aggregate results and input manifest |
| `code/` | Independent checks and aggregate-only manuscript exhibit generators |
| `replication/README.md` | Exact build and rerun instructions |
| `PACKAGE_MANIFEST.csv` | SHA-256 inventory of package files |

The final Word/PDF has 35 pages, including 21 pages from introduction through conclusion; the LaTeX rendering has 38 pages with 23 main-text pages. Both are within the mandatory 40-page maximum before appendices. Their main-text lengths are below the approximate 25–40-page guidance, disclosed rather than treated as exact compliance. Full render and source-identity checks are recorded in `audit/document_validation.json` and `audit/word_build_validation.json`.

The empirical source is pinned to [`d2d41666ed213e4cc1f6cb382313f59c29e87ea0`](https://github.com/uvangludvig-ship-it/financethesis/tree/d2d41666ed213e4cc1f6cb382313f59c29e87ea0/thesis_final). No existing analysis files are replaced by this folder.

## Access and rights

This folder adds original prose, code, aggregate outputs and source metadata. Licensed security-level LSEG/Lipper/MSCI observations and third-party full texts are not copied into this package. The input manifest identifies the exact files needed by an authorized researcher. Access must follow the relevant licenses; the presence of a file in another repository location is not permission to redistribute it.

Reproducible arithmetic is not a guarantee of valid identification or perfect data. Unresolved notice verification, holdings coverage, corporate actions and sparse bootstrap inference are documented in the report and manuscript.
