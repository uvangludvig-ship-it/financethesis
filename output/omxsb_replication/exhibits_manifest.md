# Exhibits manifest

All exhibits are produced by code/notebooks/replication_omxsb.ipynb from stocks_daily.csv.gz, stocks_static.csv, indices_daily.csv, omxsb_events_with_ric.csv and the 31 Fondinnehav zip files (2018Q4 to 2026Q2). Tables are saved as .tex (booktabs fragment), .docx and .csv in output/tables; figures as .pdf and .png (300 dpi) with their plotted data as .csv in output/figures.

| Exhibit | Files | Description |
|---|---|---|
| tab_01_sample | tex, docx, csv | Event counts by period before and after the listing/delisting filter |
| tab_02_car | tex, docx, csv | Abnormal returns around OMXSB changes by period (anchor Table 2) |
| tabA_07_car_robustness | tex, docx, csv | Table 2 under three alternative conventions: excluding the 2020-11-10 review, all announcements after close, all pre-open |
| tab_03_determinants | tex, docx, csv | Determinants of the index effect with period dummies (anchor Table 3) |
| tabA_02_isin_matches | tex, docx, csv | ISIN name matches used to bridge ISIN changes in FI holdings |
| tabA_03_index_funds | tex, docx, csv | Funds classified as OMXSB index trackers from their trades |
| tabA_04_split_factors | tex, docx, csv | Split factors applied to pre-announcement fund holdings |
| fig_01_nettrading | pdf, png, csv | Mean net trading by index funds around OMXSB changes, by year (anchor Figure 1) |
| fig_03_scatter | pdf, png, csv | Cumulative abnormal return against net trading by index funds, one point per event (anchor Figure 3) |
| tab_04_institutions | tex, docx, csv | Median net trading by fund type and year (anchor institutions table) |
| tab_05_elasticity | tex, docx, csv | Price elasticity from index-fund net trading and CAR by period (anchor elasticity table) |
| fig_08_car_announcement | pdf, png, csv | Mean cumulative abnormal return from AD−100 to AD+10 by period (anchor Figure 8) |
| fig_09_car_effective | pdf, png, csv | Mean cumulative abnormal return from ED−1 to ED+100 by period (anchor Figure 9) |
| fig_10_size_rank | pdf, png, csv | Market-cap percentile rank of added stocks in the month before the announcement, by year (anchor Figure 10) |
| fig_11_volume | pdf, png, csv | Share of volume traded on each day from ED−22 to ED+22 by period (anchor Figure 11) |
| tab_06_volume_share | tex, docx, csv | Share of 45-day volume on the days around the effective date, by period |
| tabA_06_event_chain | tex, docx, csv | Event counts through the construction chain |
| tabA_05_dropped_events | tex, docx, csv | Events dropped by the listing/delisting filter |
