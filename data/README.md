# data/: all data, gemensam för alla uppsatsalternativ

Data flyttas aldrig in i en uppsatsmapp. Den ligger här, en gång, och varje alternativ pekar hit. Undantaget är `pagaende/03_omxsb_indexeffekt/thesis_final/data/`: det är en fryst och md5-kontrollerad kopia, så att den gällande uppsatsen går att köra fristående.

- **`MANIFEST.md`** beskriver varje fil: vad den är, var den kommer ifrån och vilket skript som byggde den.
- **Den här filen** visar vilket alternativ som använder vad.

## Lagren

| Mapp | Betyder | Vem skriver |
|---|---|---|
| `raw/` | Källfiler exakt som de kom. Ändras aldrig | ingen; filer läggs in |
| `input/` | Listor byggda eller kontrollerade för hand (händelselistor, swing pricing, beställningslistor) | författarna, med byggskriptet angivet |
| `derived/` | Det som skripten i `build/` tar fram ur `raw/` och `input/` | bara skript |
| `build/` | All kod som bygger eller hämtar data i `raw/`, `input/` och `derived/`. Se `build/README.md` | – |

## Vad som används av vilket alternativ

Numren är alternativens nummer: 01 och 02 ligger i `arkiv/` (01 = FTN:s tidiga ankare, 02 = FTN-pristryck, vilande), 03 ligger i `pagaende/` (OMXSB-indexeffekten). 03h = används bara i 03:s historik.

| Mapp | Innehåll | Används av |
|---|---|---|
| `raw/ppm/` | Pensionsmyndighetens månadsstatistik per fond 2001–2026, fondlista, avgifter | 01, 02 |
| `raw/ftn/` | Fondtorgsnämndens elva upphandlingsrapporter | 01, 02 |
| `raw/fi/` | FI:s kvartalsvisa fondinnehav 2018Q4–2026Q2 | 02, 03h (FI-kontrollen i `thesis_final` har en egen härledd kopia) |
| `raw/fi_short/` | FI:s blankningsregister (hämtat 31 okt och 2 nov) | 03h |
| `raw/shof/` | SHoF:s fondregister och fältdefinitioner. `Valuations/` och `Reinvestments/` (dagliga exporter, flera GB) ligger inte i git utan delas för hand. Här ligger också pilotexporterna från 3–4 nov | 02 (tranchdagar), 03h (SHoF-piloterna); `thesis_final` har en månadskopia |
| `raw/lseg/panel_2012_2026/` | LSEG-kurspanel 2012–2026, 1 667 RIC | 02, 03h (första replikationen) |
| `raw/lseg/panel_2005_2026/` | LSEG-kurspanel 2005–2026 och fondernas dagliga NAV. **Använd parquet-filen; `stocks_daily_2005.csv.gz` är trasig som mottagen** | 03 (`thesis_final/data/prices/all_stocks_daily_*` är samma data), 02 (fond-NAV) |
| `raw/lseg/panel_eu/` | 670 europeiska aktier som förlorarfonderna ägde, plus SEK-kurser | 02 |
| `raw/lseg/datastream/` | Datastream-export 15 okt, ersatt av panelerna men sparad | – |
| `raw/lseg/klassificering/` | Sektor, marknad och free float per RIC, priser för aktier som saknas i panelen (1 nov) | 03 (kopior i `thesis_final/data/`) |
| `raw/lseg/twins/` | Kurser för tvillingaktier som saknas i panelen (1 nov) | 03 (kopior i `thesis_final/data/prices/`, steg 16) |
| `raw/ap/` | AP1–AP4:s publicerade innehavslistor (hämtade 31 okt) | 03h (`omxsb_extension_20261031`) |
| `raw/omxsb_extension_20261031/` | Originaldokument till utvidgningen 31 okt | 03h |
| `input/omxsb/` | OMXSB- och OMXS30-ändringar 2005–2026 med besked från Nasdaq, RIC-koppling, strykningsorsaker, sammansättningen juni 2009, trackerfondernas förmögenhet, kandidatlista över trackerfonder | 03 (`thesis_final/data/events/` byggdes härifrån), 02 (del 1) |
| `input/swing/` | Swing pricing-status för FTN:s förlorare och 2019 års utrensning | 02 |
| `input/holdings_external/` | Innehav för de elva förlorare som inte rapporterar till FI | 02 |
| `input/lseg/` | Beställningslistor till LSEG-hämtningarna | 02, 03 |
| `derived/ppm/` | PPM-panel per fond och månad 2018–2026 | 01, 02 |
| `derived/ftn/` | FTN-bud, korsnyckel PPM–SHoF, kategoriavgifter, omfördelning | 01, 02 |
| `derived/exit_days/` | Förlorarfondernas dagliga förmögenhet och tranchdagar | 02 |
| `derived/measurements/` | Rundmedlemskap, förlorarnas uppdelning, FI-nettoefterfrågan | 01, 02 |
| `derived/facts/` | Fyra institutionella fakta (11 okt) | 01, 02 |
| `derived/fi/` | Alla FI-innehav i långt format (LFS), byggd av replikationsnotebooken 25 okt | 03h |
| `derived/shof_monthly/` | SHoF-värderingar per månadsslut | 02 |
| `derived/ap/` | AP-fondernas svenska innehav 2013–2026 med RIC | 03h |

## Regler

1. `raw/` ändras aldrig. Varje omvandling är ett skript i `build/`.
2. En ny datafil får en rad i `MANIFEST.md` samma dag, och en rad i tabellen ovan om den är en ny mapp.
3. Filer över 50 MB går via Git LFS (`.gitattributes`).
4. Inget raderas.
