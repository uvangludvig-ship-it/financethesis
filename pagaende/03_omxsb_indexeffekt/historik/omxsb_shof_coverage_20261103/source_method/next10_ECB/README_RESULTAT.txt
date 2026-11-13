Nästa tio fonder: källgranskning, 3 november 2026. Inte uppsatstext.

52 av 100 fond-/översynsfönster klarar den separata D-grinden med levererat totalavkastningsindex och ECB:s referensvalutakurser. Detta är inte 52 ekonomiska skattningar, marknadstäckning eller power.

FI-id   Godkända källfönster av 10
51313   6
51318   4
51381   7
51449   4
51545   7
51670   7
51734   4
51776   6
60730   4
60908   3

Till täckningsgranskaren: NEXT10_D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv. Nycklar review och FI_fund_id; använd D_RIPS_ECB_source_supported. Ingen NAV-rekonstruktion används i denna kohort. Historisk klassfullständighet och klassstarter bygger fortsatt på dagens master; D_dated_lineage_verified är därför False. D_provisional_current_master är True endast för ett godkänt källfönster.

Regeln skrevs innan de nya arkivsökvägarna togs emot. Alla klassers kapital och egna RIP kontrollerades på samma faktiskt levererade datum inom fyra dagar från månadsslut; klasskapitalet konverterades konsekvent med ECB och stämdes av mot ett samtida fondkapital inom oförändrad 1-procentstolerans. Direkt SEK-kopia av fondkapital föredras, och kopior jämförs inom samma valuta. Inga äldre TNA-datum söktes för att förbättra kapitalavstämningen.

Den första, onödigt stränga exact-date-diagnostiken gav 34/100. Den är bevarad i archive_exactdate_diagnostic/. Root förtydligade före ekonomiska utfall att den redan låsta helgregeln ska gälla: för lördag/söndag används senast föregående ECB-datum, högst fyra dagar tidigare, med båda datumen redovisade. Det ger de slutliga 52/100. Saknade vardagar och ej verifierade TARGET-helgdagar fylls fortfarande inte. ECB:s referensfixing är inte bevisligen NAV-leverantörens värderingskurs; denna begränsning kvarstår.

100 fond-/översynsflaggor återaggregerades oberoende från månadstabellen. Alla endpoint- och helgvalutadatum kontrollerades. FINAL_CHECK.json innehåller resultat och SHA256 för den slutliga behörighetsfilen. FAILURE_COUNTS.csv visar kvarstående källstopp. Inga fondavkastningar, nettoflöden, kovarianser eller riskutfall räknades fram. Tidigare femfonds-D och A/B/C är oförändrade.

Körning (pandas/numpy; samma lokala runtime som föregående D):
python build_next10_D.py --valuations [Valuations-arkivet] --rips [RIPS-arkivet]
Exakta sökvägar och inputhashar finns i INPUT_LOCK.json. ECB-källmetadata finns i den angivna ECB_FX_SOURCE.json. Alla publiceringsbara filer här innehåller endast kod, tekniska anteckningar, datum, identifierare och granskningsflaggor. Råa kapital-, RIP- eller valutavärden har inte kopierats till resultaten.
