# Det optimala Klose-relaterade ämnet (7 sep 2026)

## 1. Vad Klose behöver veta

Klose är en AI-driven sell-side-rådgivare för nordiska ägarledda SME,
byggd på successionsvågen, med en plattform för värdering (DCF och comps),
köparmatchning (22 000 köpare, 10 000 precedenttransaktioner) och datarum.
Affärsmodellen vilar på fem antaganden som en uppsats kan pröva:

| # | Kloses beslutsfråga | Vad det kräver | Kan vi? |
|---|---|---|---|
| a | Vad är ett SME värt, och vad driver multipeln? (värderingsmotorn) | Transaktionspriser + bokslut för privata bolag | **Ja, nyupptäckt**: 22 % av svenska privata affärer har dealvärde i CapIQ (217 st 2025–26, median 6,6 MUSD, kvartiler 1,8–30 MUSD, exakt Kloses segment); Serrano ger EBITDA och omsättning för alla, även de 78 % utan dealvärde |
| b | Vilken köpartyp betalar mest, och när? (matchning, timing) | Priser per köpartyp över kreditcykeln | Delvis: ~2 000 svenska affärer 2015–2024 med egenberäknade multiplar, ~300 PE |
| c | Säljer stressade ägare för billigt? (säljargumentet) | Ägarålder + pris | Bara för ett delurval (Retriever) |
| d | Vad händer med bolaget efter försäljning, per köpare? | Bokslut efter affären | Ja (ämne A) |
| e | Bromsar regleringen affärerna? (ISP-anmälan) | Affärsvolymer per sektor och land | Ja (ämne F) |
| f | Hur stor är marknaden och konsolideringen? | Ägarbyten i populationen | Ja (Serrano koncernmoder; ämne G) |

## 2. Den nya kandidaten P: prissättning av privata bolag

**Titel.** *Pricing the Private Firm: Liquidity Discounts, Buyer Type and
Credit Conditions in Swedish SME Transactions, 2015–2024*

**Forskningsfråga.** *Säljs svenska privata bolag med rabatt mot jämförbara
noterade bolag, vem betalar rabatten (grundarägda, PE-ägda, dotterbolag),
vilka köpare betalar mest, och hur ändrades allt när räntorna steg 2022?*

**Varför det är Kloses fråga.** Multipelmodellen är kärnan i Kloses
värderingsprodukt, köpartypens pris över cykeln är kärnan i matchningen,
och rabatten för grundarägda bolag är säljargumentet. Uppsatsen bygger
dessutom exakt den databas Klose behöver: CapIQ-affärer kopplade till
Serrano-bokslut. Det är den enda vägen till en verklig datafördel över tid.

**Ankare (kärna, verifierade).**
- Officer (2007), *JFE* 83, 571–598: olistade bolag säljs 15–30 % billigare;
  rabatten större när kredit är dyr och säljaren behöver likviditet.
- Jaffe, Jindra, Pedersen & Voetmann (2019), *JFQA* 54, 1371–1401: rabatten
  försvinner när man rättar Officers metod (trunkering, Jensens olikhet).
- Bargeron, Schlingemann, Stulz & Zutter (2008), *JFE* 89, 375–390: PE
  betalar ~60 % lägre premier än noterade köpare.
- Axelson, Jenkinson, Strömberg & Weisbach (2013), *JF* 68, 2223–2267:
  buyout-priser drivs av kreditvillkor.
- Bodnaruk, Kandel, Massa & Simonov (2008), *RFS* 21, 2779–2824: svenska
  ägares diversifiering styr prisrabatter vid exit (svensk föregångare).
- Erel, Jang & Weisbach (2015), *JF* 70, 289–328: europeiska privata
  targets och finansiella restriktioner.

**Replikation.** Officers rabatt (privata targets mot noterade jämförbara
affärer i samma bransch, storlek och år, från CapIQ/LSEG) med både Officers
kvot och Jaffes log-multipelregressioner på samma data. Tvisten är
oavgjord utanför USA.

**Utvidgning, tre delar.**
1. **Selektionsmodellen ingen kunnat skatta.** Dealvärde saknas för 78 %
   av affärerna, men Serrano visar bokslutet för alla targets, även de
   utan pris. Vi kan alltså modellera vilka affärer som får ett publikt
   pris (storlek, köpartyp, rådgivare, lönsamhet) och korrigera rabatten
   (Heckman med verklig exklusion). Det är nytt: USA-litteraturen ser bara
   de affärer som har pris.
2. **Köpartyp × räntechocken 2022.** PE-fond, PE-plattform (add-on),
   noterad serieförvärvare, övrig strategisk; skillnad-i-skillnad före och
   efter 2022 (Axelson; Gorbenko & Malenko). Förutsägelse: finansiella
   köpares priser faller mest.
3. **Säljartyp.** Grundar-/familjeägt (aldrig sponsor-ägt i CapIQ,
   ingen koncernmoder i Serrano) mot PE-ägt mot dotterbolag; för ett
   delurval ägarens ålder från Retriever.

**Mekanism.** Likviditetsbehov (Officer) mot informationsasymmetri (Cooney
m.fl. 2009, *JFE*); köparens finansieringskostnad (Axelson) mot synergier.
Nollresultat: ingen rabatt → Jaffe har rätt även i Europa, vilket vore ett
resultat.

**Data och genomförbarhet.** CapIQ 2015–2024 (export pågår, 2–3 år per
dag), ~15 000 svenska affärer, ~2 000–2 500 med dealvärde; Serrano för
bokslut och koncernmoder; LSEG för noterade jämförbara. Namnmatchning
CapIQ → organisationsnummer (60–75 % träff). Retriever för ägarålder i
delurval.

**Risker.** Selektion i dealvärde (hanteras, och är i sig ett bidrag);
~300 PE-affärer ger begränsad styrka i räntechocktestet; namnmatchning
tar tid; identifikationen är tvärsnitt plus en DiD, svagare än I och H.

**Rubrikpoäng (egen bedömning).** Ankare 3, tidskrift/ålder 1 (2007–2019),
samma metod ny miljö 2, krok 1 (räntechocken 2022; PE-debatten), bidrag 1,
egen data med N 2, svensk data 2, två hypoteser 2, institutionsargument 1
(universella bokslut ger selektionsmodellen), kvasiexperiment 1
(räntechock × köpartyp), informativ nolla 1 = **17/20**.

## 3. Ranking av Klose-relaterade ämnen

| Ämne | Klose-värde | Rubrik | Kommentar |
|---|---|---:|---|
| **P** Prissättning av privata bolag | Högst: kalibrerar värderingsmotorn, köpartyp och timing, säljargumentet, bygger databasen | 17 | Kräver att CapIQ-exporten blir klar och matchningen görs |
| **F** Granskningslagar och SME-affärer | Högt: Klose hanterar ISP-anmälningar, ser gränsöverskridande köpare | 19 | Högst prispoäng; internationellt |
| **A** Utfall efter ägartyp | Medel: köparval, säljarens icke-prisfrågor | 15 | Svagare identifikation |
| **G** PE-plattformar och marknadsmakt | Medel: förstå plattformsköparna (38 % av affärerna) | 17 | Hög datarisk |

## 4. Rekommendation om Klose-koppling ska väga

**Ett Klose-ämne: P.** Det är det enda som direkt förbättrar Kloses produkt
och samtidigt avgör en levande akademisk tvist (Officer mot Jaffe) med
data ingen haft. **Två ämnen i synopsisen: I + P.** I är det säkra
prisämnet, P är Kloses; de delar Serrano men inte fråga, litteratur eller
data. Vill ni ha högre prispoäng på Klose-ämnet: I + F.

**Första steget för P:** avsluta CapIQ-exporten 2015–2024, matcha 200
svenska affärer med dealvärde till Serrano och räkna EV/EBITDA själva.
Ligger medianen nära CapIQ:s rapporterade 9× för privata bolag är
pipelinen rätt.
