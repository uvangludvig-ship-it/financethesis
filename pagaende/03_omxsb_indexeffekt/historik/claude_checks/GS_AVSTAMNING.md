# Avstämning mot Greenwood och Sammon (2025), analys för analys

Källa: den publicerade versionen (Journal of Finance 80(2): 657–698), fulltext i Harvards arkiv (dash.harvard.edu). Uppdaterad 2 november 2026, 19:40. Status gäller OMXSB 2007–2026.

| G&S | Analys | Vår motsvarighet | Status |
|---|---|---|---|
| Avsnitt 1.2, figur 1 | Indexfondernas nettoköp per år | `runda11_resultat/G_figur1_figur5.csv` (LSEG 2007–26); FI 2019–26 i `nettokop_v2.py` | Gjort |
| Figur A1 | Andra sätt att identifiera indexfonder | Indexfonder efter innehav (`agar_kontroll/indexfond_innehav.py`) | Gjort, med annan metod |
| Tabell 1, figur 2 | Effekt per år: besked, genomförande, totalt | Ludvigs `output/omxsb_replication_2007/` | Gjort |
| Figur 3 | CAR mot nettoköp per händelse | Runda 11 H | Gjort |
| Tabell 2 | CAR på periodkonstanter och kontroller (onormal omsättning, relativ storlek, arbitragerisk, analytiker) | Runda 11 A | Gjort |
| Avsnitt 2.2, tabell 3, figur 4–6 | Migrationer | T26, E3: inga migrationer 2007–26 | Gäller inte Sverige, mätt |
| Figur 7 | Kursbanan AD−100 till AD+14 | Runda 11 I (`I_figur7.csv`) | Gjort |
| Tabell 4 | Uppgång [AD−n, AD−1], n = 10, 20, 50, 100 | Runda 11 B | Gjort |
| Figur 8 | Storleksrang för tillagda bolag | Ludvigs E4c | Gjort |
| Tabell 5 | M per period | Runda 11 C (och T24) | Gjort |
| Avsnitt 2.4.1 | M i långt fönster | Runda 11 C och D | Gjort |
| Tabell 6 | M med kontroller | Runda 11 D (H11a, H11b) | Gjort |
| Figur 9 | Effektiv spread | Ludvigs E2 (noterad spread) | Gjort, med noterad i stället för effektiv spread |
| Avsnitt 2.4.3 | Implementation shortfall (Virtu) | Ingen data | Går inte |
| Avsnitt 2.4.3 | Volym koncentrerad till händelsen | Ludvigs E5 | Gjort |
| Tabell 7 | Ägarförändring: indexfonder, passiva, aktiva, alla institutioner | Runda 11 E (fonder i LSEG) | Gjort för fonder; övriga institutioner saknas |
| Avsnitt 2.4.3 | Nyemissioner kring indexändringar | Runda 11 F | Gjort |
| Avsnitt 3, tabell 8 | Andra index | T28 (OMXS30), småbolagsindex i T26 | Gjort, för lite styrka för OMXS30 |
| Tabell A1, A2 | Urvalsfilter och känslighet för urval | Ludvigs urval och flaggfil; runda 11 med och utan splittade aktier | Gjort |
| Internet Appendix | Separat M för migrationer och direkta tillägg | Inga migrationer | Gäller inte |

**Avvikelser i metod som ska nämnas i uppsatsen**
- Marknadsjustering mot .OMXSBGI (G&S: S&P 500).
- D ur LSEG/Lipper-fonder, mätt före AD och efter ED (G&S: Thomson S12 kvartalet före och efter).
- Händelser där aktien senare splittats utesluts, eftersom LSEG:s innehav är justerade för splittar men aktieantalet är historiskt.
- Analytiker = antal vinstprognoser i senaste månaden före AD (G&S: IBES vid senaste rapport före ändringen).
- Perioder om fem år, 2007–2026 (G&S: decennier, 1980–2020).
