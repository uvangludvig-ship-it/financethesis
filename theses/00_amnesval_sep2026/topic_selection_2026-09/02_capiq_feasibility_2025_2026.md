# CapIQ-feasibility: svenska targets 2025–2026 (mätt 6 sep 2026)

Källa: `~/dev/capiq-transactions/exports/capiq_ma_dach_nordics_{2025,2026}.xls`
(6 914 deals DACH + Norden). Skript: inline pandas via `build_db.read_export`.

## Täckning, hela exporten

| Variabel | Täckning |
|---|---|
| Köpartyp (strategisk/finansiell) | 92 % |
| Target privat bolag | 71 % |
| Deal value | 17,7 % |
| Implied EV | 16,2 % |
| Target LTM-omsättning | 17,4 % |
| Target LTM-EBITDA | 5,0 % |
| EV/EBITDA | 2,8 % |
| EV/Revenue | 6,2 % |
| Premie 1 dag (noterade) | 2,3 % |
| Earnout-belopp | 2,9 % |
| Rådgivare till target / säljare / köpare | 15 % / 13 % / 34 % |
| Säljare namngivna | 26 % (svenska privata) |

Targetländer: Tyskland 2 796, Sverige 1 375, Finland 666, Norge 648,
Danmark 569, Schweiz 566, Österrike 263, Island 31.

## Svenska privata targets: 968 av 1 375 svenska targets

Köparklassificering (egen regel: köparens `ownership_status` innehåller
"Current Sponsor" → PE-ägd plattform; `buyer_type` Financial Buyer eller
`company_type` Investment Firm → PE-fond direkt; `company_type` Public
Company utan sponsor → noterad strategisk; övrigt → övrig strategisk):

| Köparklass | Antal | Andel | Median target-omsättning (USDm, där känd) |
|---|---:|---:|---:|
| PE-ägd plattform (add-on) | 370 | 38 % | 8,1 |
| Övrig strategisk (privat/oberoende) | 409 | 42 % | 6,5 |
| PE-fond / finansiell köpare (plattformsköp) | 113 | 12 % | 22,3 |
| Noterad strategisk (ej sponsor-ägd) | 76 | 8 % | 7,8 |

Mest aktiva köpare av svenska privata bolag 2025–2026: XPartners Group (12),
Citira Holding (11), KEYTO Group (10), Ahlsell (8), Nimlas (8), Circura (6),
Qflow (6), Selatek (6), Aderian (5), Monterro (5), White Pearl (5),
Aterion (5), Lagercrantz (5), Axcel (5). Vanligaste sponsorer bakom
add-ons: Norvestor, Axcel, Fidelio, Celero, Amplio, Nordstjernan/Adelis,
Searchlight.

Köpare med ≥3 affärer på två år står för 22 % av affärerna; ≥5 affärer för
12 %.

Köparens HQ: Sverige 701, USA 39, Norge 36, Finland 32, Tyskland 24, UK 17.
Status: Closed 707, Announced 251, Cancelled 6 (placebo-gruppen "annonserad
men ej fullbordad" blir liten, komplettera med Serranos koncernregister).

## Konsekvens för ämnesvalet

- Prisstudier på privata bolag är uteslutna (multiplar för ~3 %).
- Utfallsstudier via Serrano är fullt möjliga: ~1 000 svenska privata
  targets per år, ~8 000–9 000 för 2015–2023.
- Den intressanta tredelningen är inte "PE mot strategisk" utan
  **PE-ägd plattform (add-on) mot PE-fond direkt mot oberoende strategisk
  köpare mot noterad serieförvärvare.** Add-ons är den enskilt största
  kanalen, ligger närmast Kloses kundsegment (median omsättning ~8 MUSD) och
  saknar kärnartikel om europeiska målbolags utfall.
- CapIQ:s `buyer_type` klassar plattformar som "Strategic Buyer";
  klassificeringen måste göras via köparens sponsor-status och verifieras
  manuellt för ett urval.

## Bakgrundsfakta från Riksbankens staff memo "Private equity in Sweden: a financial stability perspective" (2025)

- Sedan 2010 har PE-bolag förvärvat cirka 3 400 svenska bolag via buyouts
  (PitchBook); bolag med buyout senaste sju åren sysselsätter nära 364 000.
- Flest nya PE-investeringar 2021; tydlig avmattning 2022 med stigande räntor.
- Kärnä & Myers (2025): ~4 000 svenska LBO:er 1990–2022, Serrano + PitchBook,
  matchad DiD: kortfristig skuld +~20 %, försäljning och tillgångar växer,
  långfristig skuld ökar inte (rollover inom 12 månader), räntekostnader upp.
- Memot beskriver "add-on strategy" som en av PE:s huvudstrategier men
  analyserar inte add-ons separat, och jämför inte PE mot strategiska eller
  noterade serieförvärvare. Det är luckan vår uppsats fyller.
- Källa: riksbank.se, staff memo 2025 (PDF sparad i sessionens scratchpad
  som riksbank_pe.txt).

## Tillägg 6 sep kväll: utfallsvariabler för granskningslags-idén (F)

- Andel utländska köpare (köparens HQ ≠ targetland), 2025–2026: Österrike
  73 %, Danmark 62 %, Schweiz 60 %, Tyskland 50 %, Norge 49 %, Finland 38 %,
  **Sverige 28 %**. Andel köpare utanför EU/EES/Schweiz: Sverige 12 %,
  Tyskland 25 %, Österrike 25 %, Danmark 19 %.
- **Tid från annonsering till stängning är oanvändbar som utfall för
  privata affärer:** 87 % av affärerna har samma annonserings- och
  stängningsdatum (CapIQ registrerar SME-affärer vid stängning). Utfall för
  F måste därför vara affärsvolym och sammansättning (utländsk andel,
  PE-andel, köparland), inte handläggningstid. Avbrutna affärer: 30 av
  6 914, för få för placebo.
- Bransch saknas för 28 % av svenska targets i CapIQ; sektorklassificering
  för Sverige bör göras via Serranos SNI-kod efter matchning, för övriga
  länder via CapIQ:s branschfält.
