# under_utredning/: nya alternativ som prövas

Tom just nu. Här läggs ett nytt uppsatsalternativ medan det utreds, alltså ett nytt ämne, ankare eller en ny metod. Det flyttas till `../pagaende/` om ni väljer det och till `../arkiv/` om det läggs ned. Hela mappen flyttas och numret behålls.

## Så startar ni ett nytt alternativ

1. Skapa `under_utredning/NN_kort_namn/` med nästa lediga nummer. 00–03 är tagna, så nästa är 04.
2. Kopiera mallen nedan till `NN_kort_namn/README.md` och fyll i den.
3. Lägg kod i `NN_kort_namn/kod/` och resultat i `NN_kort_namn/output/`.
4. Data läggs i den gemensamma `../data/`, aldrig i alternativets mapp. Rådata hamnar i `data/raw/`, byggskript i `data/build/`, en rad läggs i `data/MANIFEST.md` och alternativets nummer skrivs i "Används av" i `data/README.md`.
5. Lägg till en rad i tabellen i repots `README.md`.

## Mall för README

```
# NN Kort namn

**Status:** UNDER UTREDNING / PÅGÅENDE / VILANDE / ÖVERGIVET / AVSLUTAT, sedan <datum>. <En mening om varför.>
**Senast ändrad:** <datum>, <vem>

## Frågan
<En eller två meningar.>

## Ankare och metod
- Ankare: <författare (år), titel, tidskrift>
- Metod: <t.ex. eventstudie, DiD, replikation av tabell X>
- Data: <vilka mappar i data/ som används>

## Det som gäller
| Vad | Var | Kommentar |
|---|---|---|
| Kod och resultat | `kod/`, `output/` | hur man kör, vad sista raden ska säga |
| Text | `.../` | |

## Hur man kör
<kommandon>

## Historik (gäller inte)
| Datum | Mapp | Vad | Utfall eller beslut | Status |
|---|---|---|---|---|
```

Statusord:
- **UNDER UTREDNING**: prövas; ligger i `under_utredning/`.
- **PÅGÅENDE**: detta skriver vi; ligger i `pagaende/`.
- **VILANDE**: kan tas upp igen, inget är fel; ligger i `arkiv/`.
- **ÖVERGIVET**: valdes bort, med skäl; ligger i `arkiv/`.
- **AVSLUTAT**: klart, till exempel ämnesvalet; ligger i `arkiv/`.
