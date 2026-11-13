# Identity correction after independent audit

Exploratory correction, 2026-11-01. Results of the original run and the independent identity correction were already observed. This is not a new blind test.

The independent screen examined all 452 frozen events and all six pairs of the event/control roles (2,712 pairs), using shared static ISIN and identical pre-event close/total-return/volume history. Two self-controls were identified and primary-source confirmed:
- OMXSB-2019H1-06: NYFO.ST versus ALTRAF.ST. Nasdaq notice 13 May 2026, effective name change 15 May 2026, unchanged ISIN SE0011426428: https://view.news.eu.nasdaq.com/view?id=bf5badbacea6190ca2736e6094e4251c6&lang=en
- OMXSB-2026H1-07: MAHAa.ST versus KEOC.ST. Issuer notice 9 June 2026, unchanged ISIN: https://view.news.eu.nasdaq.com/view?id=b52a78d490c9dabac52116c623c7199fd&lang=en

Exclude each entire event for every horizon, model and control-count variant. Do not substitute new controls, change the contrast, winsorize returns or remove actual corporate news. All original results remain under ../persistence/. These exclusions repair the event sample but do not certify all historical issuer mappings or main-list eligibility.

Independent audit noted a shared missing-return day in 2025 and real corporate news in long windows. Do not impute returns or remove economically real movements. Keep complete-case attrition and interpretation limitations explicit.
