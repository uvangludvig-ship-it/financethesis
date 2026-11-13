# Första steget, version 2, regler bestämda 2026-11-01 22:35 CET innan beräkningen

**Redan känt:** gamla beräkningen ger 0,741 % (24 händelser 2019–2026, alla med väntat tecken). Kända fel: NCC och Corem har systerslagets eller annat aktieslags ISIN i indexslagets lista; Bonava, Sweco och Stora Enso saknar systerslagets ISIN; indexfonder identifierade med grovt textmönster.

**Indexfonder (strikt):** jämförelseindex innehåller "OMX Stockholm Benchmark", "OMXSB" eller "SBX", och inte "ESG", "Custom", "Responsible" eller "Sustainability"; och antingen aktiv risk ≤ 0,5 eller ett namn som innehåller "index", "indexnära", "passiv" eller "access" (men inte "edge"). **Bred definition** (känslighet): alla fonder vars jämförelseindex innehåller OMXSB-familjen, inklusive ESG- och anpassade varianter, med aktiv risk ≤ 1,5.

**Aktieslag:** ISIN per aktieslag tas från FI:s instrumentnamn (bolagsnamn och aktieslag) och kontrolleras mot panelens ISIN. Indexslagets och systerslagets ISIN-listor får inte överlappa; varje händelse redovisas med ISIN och instrumentnamn.

**Mått:** summan av indexfondernas innehav i aktieslaget vid sista kvartalsslutet före AD och första kvartalsslutet efter ED. Förändringen anges i procent av aktieslagets antal aktier (panelen, kvartalet efter). Systerslagets förändring i samma enhet. Tecken vänt för borttag. Redovisas per händelse och per fond, med medel och median, för strikt och bred definition. Avståndet i dagar mellan kvartalsslut och händelse redovisas.

**Förtydligande 22:41 CET, innan något utfall beräknats:** listan över fonder visade att blandfonder med ett sammansatt jämförelseindex (till exempel Swedbank Robur Access Mix, Transfer 50, KPA Blandfond, Länsförsäkringar Sparmål) kommer med i den strikta definitionen. Strikt kräver därför också att jämförelseindexet bara består av OMXSB-familjen (en komponent, eller vikt 100). Den breda definitionen är oförändrad.

**Tillägg 23:30 CET, vid genomgång av koden:** den breda definitionen i körningen tog med fonder som saknar uppgift om aktiv risk i FI-data (107 fondkvartal av 957). Deklarationen säger aktiv risk ≤ 1,5. Avvikelsen gäller den breda definitionen i första steget v2 och klassningen av ESG-indexfonder i T16. Den strikta definitionen påverkas inte. `fi_klass.py` återskapar körningens klassning exakt och kommenterar avvikelsen.
