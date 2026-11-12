# OMXSB thesis research draft

Complete English working draft of **Index Reconstitutions and Stock Returns in Sweden**, with its computational audit and reproducibility materials. Prepared on 12 November 2026 for Alexander Fox and Ludvig Pauli Uväng.

Read [the PDF](manuscript/main.pdf), then [the verification report](audit/verification_report.md). Editable source starts at [main.tex](manuscript/main.tex). The draft separates descriptive return associations from causal effects and labels all new analyses as exploratory.

**Submission status:** this is an AI-generated research draft. The BE451 Autumn 2026 syllabus permits disclosed AI assistance but prohibits AI directly writing thesis text. The authors must write the submitted text and verify the argument and sources. The PDF contains a full disclosure. This package does not represent a submission-ready or independently certified thesis.

## What the evidence supports

- Lower latest-period addition returns than in the unusually high earliest period, without a monotonic decline.
- A positive later-decade addition association; insufficient precision to establish disappearance in the latest block.
- Measured benchmark-linked holdings changes and concentrated trading before effectiveness, without an identified causal mechanism.
- An exploratory fixed-cohort cumulative-return result through ED+20. Persistence at a finite horizon is not permanent or causal price impact.

## Find the supporting material

| Location | Contents |
|---|---|
| `manuscript/` | Complete text, bibliography, generated tables, figures and PDF |
| `audit/verification_report.md` | Completed checks, discrepancies and unresolved issues |
| `audit/results/` | Independent return, dependence, horizon, ratio, multiplicity and equivalence calculations |
| `audit/analysis_addendum.md` | Dated exploratory specification and subsequent changes |
| `audit/exhibit_map.csv` | Exhibit-to-input map |
| `sources/` | Reference ledger, notice retrieval outcomes, data dictionary and structure benchmark |
| `replication/thesis_final/` | Frozen original code, declarations, aggregate results and input manifest |
| `code/` | Independent audit and manuscript exhibit generator |
| `replication/README.md` | Exact build and rerun instructions |
| `PACKAGE_MANIFEST.csv` | SHA-256 inventory of package files |

The empirical source is pinned to [`d2d41666ed213e4cc1f6cb382313f59c29e87ea0`](https://github.com/uvangludvig-ship-it/financethesis/tree/d2d41666ed213e4cc1f6cb382313f59c29e87ea0/thesis_final). No existing analysis files are replaced by this folder.

## Access and rights

This folder adds original prose, code, aggregate outputs and source metadata. Licensed security-level LSEG/Lipper/MSCI observations and third-party full texts are not copied into this package. The input manifest identifies the exact files needed by an authorized researcher. Access must follow the relevant licenses; the presence of a file in another repository location is not permission to redistribute it.

Reproducible arithmetic is not a guarantee of valid identification or perfect data. Unresolved notice verification, holdings coverage, corporate actions and sparse bootstrap inference are documented in the report and manuscript.
