# MSCI-tvillingar (T18), 2 november 2026

Testet är deklarerat i `msci_deklaration.md` (09:30), innan några kurser setts.

## Filer

- `lists_2007_2011.csv`, `lists_2012_2016.csv`, `lists_2017_2021.csv`, `lists_2022_2026.csv`: MSCI:s publika ändringslistor för Sverige, Standard (`STPublicList`) och Small Cap (`SCPublicList`), en rad per ändring. Avskrivna från MSCI:s PDF:er (www.msci.com/eqb/gimi/stdindex/ och /smallcap/) 2 november 09:17–09:28. 79 av 80 listor finns; småbolagslistan för februari 2007 saknas. Där tillägg och borttag låg på samma rad i PDF:en är de fördelade med hjälp av listans sammanställning per land; det står i kolumnen `note`. En rad är markerad `uncertain` (PPI Public Property, augusti 2026).
- `msci_sweden_changes_2007_2026.csv`: de fyra listorna sammanslagna, 523 ändringar.
- `msci_tvilling_kandidater.csv`: 41 händelser där ett aktieslag ändras och bolagets andra noterade slag inte ändras i samma översyn (26 Standard, 15 Small Cap). Uppställd för hand från listorna och panelens RIC.
- `msci_lseg_CodeBook.ipynb`: hämtar dagliga kurser, totalavkastning och volym för båda aktieslagen från LSEG.
- `write_msci_csv.py`, `build_msci_csv.py`: skripten som skrev två av listfilerna. Skripten för de andra två perioderna skrevs över under arbetet; CSV-filerna är det som gäller.

## Ordning

1. Kör `msci_lseg_CodeBook.ipynb` i CodeBook och lägg `msci_tvilling_priser.csv` här.
2. Steg 1 enligt deklarationen: första steget (omsättning) och styrkekontroll. Testet körs bara om villkoren håller.
