**FTN anchor research — 4 October 2026**

Start with [RECOMMENDATION.md](RECOMMENDATION.md). It recommends Cookson et al. (2021), *Best Buys and Own Brands*, as the strongest intellectual anchor for a focused FTN selection-spillover thesis. It gives the research question, comparison with alternatives, replication mapping, design, weaknesses and changes needed in the existing PLAN. The recommendation is conditional on verifying licensed monthly data and the course’s interpretation of an adapted replication; it does not claim a perfect or fully cleared design.

Read [DATA_AUDIT.md](DATA_AUDIT.md) for downloaded-file evidence, actual historical fund matches, variable construction and unresolved coverage. Read [WINNERS_AND_EXAMINER.md](WINNERS_AND_EXAMINER.md) for concrete thesis comparisons, limitations of the award labels, and verified examiner research.

The previous anchor’s `data/` files were not read or changed. The original README and PLAN were not replaced. Existing deletions and untracked material under `data/` predate this review.

**What was done**

- Read repository planning and course material, including original research-assignment slides and the synopsis.
- Audited the 660-record thesis catalogue and extracted-text collection; reviewed awarded abstracts and selected close comparisons. This was not a close reading of every thesis.
- Researched candidate anchors through published articles, author manuscripts and institutional sources; read the Cookson manuscript for its actual empirical design.
- Checked Sabbatucci’s official profile and current research list, distinguishing working papers from publications and facts from inferences about relevance.
- Downloaded fresh public FTN, FI and PPM sources; parsed spreadsheet cached values without executing macros; verified current and historical identity/asset/price matches.
- Produced research notes and reproducible availability checks. No treatment-effect regression, statistical-power certification, licensed data download, communication to another person, or thesis submission was performed.

**Reproduce the audit**

From the repository root, run:

```sh
python3 research/anchor_review/audit_sources.py
```

Python’s standard library is sufficient. The script reads local downloaded sources and the existing text catalogue. It does not access `data/` or the network. It recreates:

| File | Purpose |
|---|---|
| [public_data_audit.json](public_data_audit.json) | June 2026 exact ISIN coverage and source rows, including the narrow single-class subset |
| [historical_public_probe.json](historical_public_probe.json) | One selected fund’s 2023–2024 identity, asset and NAV availability |
| [shof_master_probe.json](shof_master_probe.json) | Public Morningstar identity-master check; not historical valuation access |
| [corpus_inventory.csv](corpus_inventory.csv) | Reproducible thesis labels and limited text measures |
| [corpus_summary.json](corpus_summary.json) | Same-year descriptive comparisons and their limitations |
| [source_sha256.json](source_sha256.json) | Checksums of the downloaded source files and local PDF text extractions |

Download locations and access dates are recorded in [source_urls.json](source_urls.json). The `.txt` files beside three PDFs are local `pdftotext` derivatives of those PDFs. The exploratory `winner_metrics.csv` and `comparison_metrics.csv` were generated with the repository’s pre-existing metrics script; several of that script’s measures are fragile and were deliberately excluded from the conclusions.

**Important interpretation limits**

The public-data matches are an availability audit, not a complete sample or a proof of power. Reported holdings are stocks. Provider flow series can be estimates. Exact share-class matches do not by themselves establish portfolio-wide comparability. The awarded collection is not a randomized or exhaustive prize dataset, and the comparison collection is not a verified low-grade group.

The main unresolved practical check is a working, usable SHoF/Morningstar export for the proposed cohort and comparison funds. Its source and relevant fields are documented; the group’s entitlement and historical coverage have not been authenticated. No original UK replication data were obtained. The reports make these constraints explicit rather than inferring availability from a paper title or a database catalogue.

**AI/research-use record**

These files were produced with AI assistance for source discovery, research-design critique, public-data parsing and comparative research notes. They are not student-authored thesis prose and should not be submitted verbatim as such. Keep this work in the project’s AI-use record and follow the course’s disclosure requirements. Literature claims and eventual empirical results remain subject to the authors’ own verification.
