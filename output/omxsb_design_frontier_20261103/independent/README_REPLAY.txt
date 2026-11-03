Tekniskt beslutsunderlag och metadataaudit. Ingen uppsatstext eller utförd fondflödes-/riskanalys.

Arbetskatalog:
/Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/design_frontier_20261103/independent

Runtime:
/Users/ludviguvang/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
Paket: pandas, numpy, openpyxl. Inget paket installerades för detta arbete.

Reproducerbar körordning:
1. metadata_probe.py
2. source_feasibility.py
3. freshness_metadata.py
4. dominant_source_diagnostic.py

Kör endast med samma lokala licensierade filer angivna i input-lockfilerna. Inga rådata ska kopieras till ett publikt paket. Alla utdata och skript ligger i denna katalog; repositoryt läses endast.

Lockfiler skapas innan respektive databeräkning; skriptens slutliga hashar finns i FILE_LEDGER.json. Omkörning skriver om denna arbetskatalog och tidsstämplar, inte repositoryt.

Källgrindens datum tolererar fyra kalenderdagar endast som preliminärt närvaroprov. Månadsfilerna anger inte tillräckligt exakt TNA/TRI-observationsdatum för att godkänna flöden. Slutlig riskanalys måste ha en separat daterad specifikation, källvalidering och samplerapport före första utfallsberäkning.

NF-fält lästes endast som närvaroflaggor, aldrig numeriskt summerade för ett resultat. TRI lästes i source_feasibility.py bara för positiv/ändlig närvaro, aldrig för att beräkna fondavkastning. Inga FTN-händelsedatum eller FTN-utfall lästes.

Bevarad negativ evidens:
- Strikt vendor-NF-väg otillräcklig; allmissing-NF kan bli noll i gammal månadsbyggare.
- Ny rå-ZIP undersökt, men ingen 24-månaders komplett fund-NF-historik på matchade klasser.
- TNA+TRI-väg har partiell, inte representativt verifierad, kapitaltäckning.
- Flera rimliga reparationer finns men har inte blandats in efter något riskutfall.
- Originalartikeln prövade redan indexinträden med nollresultat; inget nyhetsanspråk på den internationella frågan.

Rapportens kapitalandelar är inom den observerade svenska FI-fondpopulationen. De är inte andelar av hela börsvärdet eller all internationell fondförmögenhet. Medel över eventaktier är inte ett hopslaget kapitalviktat belopp.

Kommande avgränsade SHoF-pilot:
ACQUISITION_PILOT_CLASSES.csv och ACQUISITION_PILOT_IDS.txt beskriver20klasser i5fonder; exakt2017-01-01–2023-12-31.
ACQUISITION_PILOT_MANIFEST.json anger källfält och begränsningar. Ingen nyfil har laddats ner när denna rapport färdigställs; väntar på användarens autentisering i roots browserflöde.
validate_acquisition_pilot.py --valuations /absolut/sökväg/fil.zip --rips /absolut/sökväg/fil.zip
Skriptet är verifierat med sju syntetiska källfelstester (test_pilot_validator.py), men inte kört mot kommande verkliga filer. Skriptet accepterar också en källa i taget. Det skriver metadata i arbetskatalogen, aldrig om råfilerna. Det utför inga avkastnings-/flödes-/riskberäkningar.
