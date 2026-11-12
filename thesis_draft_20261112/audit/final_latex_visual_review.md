# LaTeX PDF visual and narrative review

## Final verification: both corrections passed

The rebuilt `thesis_draft_20261112/manuscript/main.pdf` has **38 pages**, SHA-256 **`142144d5eff1fd02f4500a94a90c104d2bac8cd6dab308e491e375a3ff6e5e21`**. Bundled Poppler rerendered PDF pages **20–25 and 36–38** at 100 dpi; all nine were visually inspected individually. The renders and fresh complete text extraction are in `final/`.

- The comparison paragraph now appears under Section 4.7 on PDF page 21. Its continuation leads naturally into Discussion on PDF page 22. The isolated paragraph page is gone; no new isolated heading or paragraph page was introduced across pages 20–25.
- Figure A1 on PDF page 37 now shows the complete vertical title **“Quoted closing spread (%)”**. Both appendix figures and their captions are readable and unclipped.
- PDF pages 36–38 have clean appendix table, figure, disclosure and page-number placement. No material clipping, overlap or detached caption was observed in the rerendered pages.
- The complete final text has no unresolved `??`, author placeholders, TODO/TBD, replacement-character or black-square markers. The final page-level glyph-boundary check reports zero out-of-page text characters.
- Final pagination: cover PDF 1; abstract PDF 2; main text PDF **3–25 = 23 pages**; references PDF 26–27; appendices PDF 28–38. Do not describe the main text as exactly 25 pages or add padding to inflate it.

**Final disposition: no remaining material layout blockers observed.** This combines the full 39-page predecessor review with the targeted nine-page review of the changed/reflowed final PDF. No manuscript/source edits were made by this reviewer. The narrative assessment below remains applicable.

## Initial full review record

Reviewed 12 November 2026. Initial source: `thesis_draft_20261112/manuscript/main.pdf`, 39 pages, SHA-256 `5e06a0226bf693fc72794118dd77129ced14751b86cc3c7ac851e1865f865a67`. The initial observations below are retained as a review trail; their two material issues were corrected and rechecked above.

## Review coverage

- Rendered **all PDF pages 1–39** with bundled Poppler at 100 dpi, saving `page-01.png` through `page-39.png` in this directory.
- Visually inspected every page in contact sheets `contact_01_06.png`, `contact_07_12.png`, `contact_13_18.png`, `contact_19_24.png`, `contact_25_30.png`, `contact_31_36.png`, and `contact_37_39.png`.
- Inspected individual full-page renders for PDF pages **3, 4, 5, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29, 31, 33, 34, 35, 36, 37, 38**. These cover all six figures, all especially dense tables, the opening narrative, discussion ending and conclusion, and the two suspect layouts.
- Extracted text from all 39 pages to `text.txt`. Checked for unresolved `??`, author placeholders, TODO/TBD, replacement characters and black squares: zero occurrences. A separate glyph-boundary check found no page-level out-of-bounds text; this does not detect clipping inside embedded figures, which required visual review.
- Pagination: cover PDF 1; abstract PDF 2; introduction through conclusion PDF **3–26 = 24 pages**; references PDF 27–28; appendices PDF 29–39. This is approximately the course's 25-page lower guidance, not exactly 25 main-text pages. Do not pad to change that count.

## Material issues to correct

1. **PDF page 22, printed page 21: isolated final Results paragraph.** The entire page contains only the 70-word size-screened comparison paragraph beginning “A separate size-screened comparison provides a complementary check.” Most of the page is blank, and Discussion begins on the following page. The forced `\clearpage` before Discussion in `main.tex` line 58 contributes to the isolated page. Allow Discussion to follow, or refit the final Results paragraph onto the previous page. This is a layout issue, not a request to add content.

2. **PDF page 38, printed page 37: clipped Figure A1 vertical axis title.** The closing-spread chart's long vertical title is cut at its upper end; it reads “Value weighted quoted closing spread (” with the unit ending missing. The axis title needs a shorter label (for example, “Quoted closing spread (%)”) or a corrected source figure bounding box. Figure A2 below it is clean.

**Initial disposition, superseded by the final verification above: needed these two layout corrections and a targeted rerender/review.** No other material clipping, collision, cropped table, unreadable figure axis, detached caption, unresolved cross-reference, or missing-label defect was observed.

## Other layout observations

- Figures 1–4 have visible scales, legends and captions. Figure 1 uses a common scale for additions and deletions; Figure 4's caption explicitly explains its nonzero starting value and pointwise intervals.
- Main Tables 1–10 and Appendix Tables A1–A12 are legible and have titles and explanatory captions. Table A1 has narrow-column hyphenation but no clipped text. Numeric columns and intervals fit.
- PDF pages 15 and 20 are float pages with two exhibits. They interrupt ongoing prose but remain readable, have complete captions, and are not material defects. Page 25 opens with two continuation lines from the preceding discussion paragraph; the subsection follows naturally.
- References wrap long URLs inside margins. Cover and appendix accurately label the file as an AI-assisted research draft rather than a compliant submission.

## Narrative judgment

The revised opening is materially stronger than the earlier mechanical version. It begins with the demand-versus-price-response puzzle, states the Swedish research question and later-decade return answer on the first text page, then connects that result to measured purchases, trading, timing and share classes. The findings are no longer framed primarily as a collection of diagnostic restrictions.

The conclusion answers the opening question in the same units and scope: positive later-decade addition returns remain; the latest block is uncertain; measured fund purchases accompany the returns; the timing and share-class results constrain interpretation without identifying a cause. The Discussion makes the pooled-US/migration distinction explicit and avoids claiming all Swedish events are verified direct additions. The prior “lower bound on net demand” and causal twin-share upper-bound problems are addressed directly.

There is still deliberate repetition of the observational/causal boundary, but the story now remains discernible through it. I found no material narrative inconsistency requiring a further conceptual rewrite in this visual-QA pass. This is a narrative/layout assessment, not fresh verification of every empirical estimate or source.
