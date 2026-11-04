Avgränsad institutions- och källkontroll, 3 november 2026.

Läs REPORT_SV.txt först. Detta är arbetsmaterial och inte uppsatstext.
Ingen ny ekonomisk utfallsanalys, ingen API-körning och ingen kontakt med externa personer.

build_note.py återskapar tabeller från den tidigare frysta filen
work/omxsb_history_extension_20261103/sources/REVIEW_VERIFICATION.csv.
Filen ligger relativt samma work-katalog. Källsammanfattningar är manuellt granskade primärkällor, inte automatiska sökresultatsklassificeringar.

archive_sources.py får bara hämta de redan dokumenterade offentliga URL:erna till private/.
Den körs separat och ingår inte i någon utfallsanalys. Eventuellt misslyckad direktnedladdning skiljs från lyckad läsning via webverktyget.

Endast exakta relativa filer i PUBLICATION_ALLOWLIST.json får publiceras.
PUBLICATION_SHA256.json innehåller alla tillåtna filers SHA256 utom sin egen, för att undvika självreferens.
Inga globmönster eller undermappar följer implicit med. private/ och fullständiga PDF/HTML-källor är alltid uteslutna.
