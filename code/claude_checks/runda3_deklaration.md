# Runda 3, deklarerad 2026-11-01 22:12 CET, innan något körs

Syfte: pröva kontrollgruppens trovärdighet, som är den största kvarvarande svagheten.

**Redan kända resultat:**
- T5v (verifierad kontrollgrupp), tillägg efter 2017, CAR [AD−1, ED+1]: +1,53 (0,36 till 2,69); bara huvudlistan +1,39 (0,15 till 2,64); ED+20 +2,24 (0,65 till 3,82). Före 2017 +3,90 (0,06 till 7,74).
- Balans efter 2017: uppgång [AD−100, AD−1] median 13,0 % för tillägg mot 0,4 % för nästan tillagda.
- Diagnostik med den gamla kontrollgruppen (före verifieringen): med nästan tillagda vars uppgång låg inom tilläggens 10–90-percentil blev skillnaden +1,23 (−0,11 till 2,57).
- T6 steg 1: regeln väljer 54 % av tilläggen efter 2017 (90 av 168) och 38 % före; den väljer i snitt 25 icke-medlemmar per översyn efter 2017 som inte lades till.

**Gemensamt:** som runda 2 (verifierad medlemslista, First North utesluten, osäkra utesluts, inga händelser i översynen före, samma eller efter, inte samma bolag som en händelseaktie). Kluster på översyn, restriktiv wild cluster bootstrap, 95 % intervall med t(G−1). Ett intervall som innehåller 0 betyder "inte påvisat".

## T12. Gemensam uppgång (common support)

- Urval som T5v. Nästan tillagda behålls bara om deras uppgång [AD−100, AD−1] ligger mellan 10:e och 90:e percentilen av tilläggens uppgång i samma period (före respektive efter 2017).
- Uppgången kontrolleras med femtedelar (gränser från tilläggens kvintiler i perioden) i stället för linjärt. Övrigt som T5: log börsvärde och fasta effekter per översyn.
- **Primärt:** tillägg efter 2017, CAR [AD−1, ED+1]. **Sekundärt:** ED+20; före 2017; borttag (spegelvänt: nästan borttagna inom borttagens 10–90-percentil).
- Balans redovisas (median uppgång, log börsvärde, log omsättning) före och efter begränsningen.

## T13. Mot Nasdaq-regelns nästan valda (T6 steg 2)

- Regeln som i T6 steg 1. Jämförelsegrupp: icke-medlemmar som inte lades till, inte bland de 30 % minst omsatta, och som antingen valdes av regeln eller hade en kumulativ andel av supersektorns fritt flytande börsvärde på högst 95 %.
- CAR = b·Tillägg + uppgång + log börsvärde + log omsättning + fasta effekter per översyn.
- **Primärt:** efter 2017 (träffsäkerhet 54 %), [AD−1, ED+1]. **Sekundärt:** jämförelsegruppen "regeln valde men Nasdaq lade inte till"; ED+20; före 2017 (träffsäkerhet 38 %, under gränsen, redovisas men vägs lätt); T13 med samma begränsning av uppgången som T12.

**Tolkning, bestämd i förväg:** har b undre gräns över 0 i både T12 och T13 (primärt) håller avkastningsskillnaden även mot kontrollgrupper med jämförbar uppgång respektive jämförbar ställning enligt regeln. Annars redovisas det som att skillnaden inte är påvisad mot den kontrollgruppen.
