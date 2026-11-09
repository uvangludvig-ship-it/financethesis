# Alla tabeller och figurer i ett Word-dokument, i Greenwood och Sammons ordning (samma ordning som filnamnen 01–12).
# Varje del byggs av sin egen fil (build(doc)), så en ändring görs bara på ett ställe.
# Körs från thesis_final efter 01–06: python3 code/output/99_all_tables.py
import sys, importlib.util
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from docx.enum.text import WD_BREAK
from _style import new_document, save

FILES = sorted(p for p in HERE.glob('[0-9][0-9]_*.py') if p.name != Path(__file__).name)
assert [p.name[:2] for p in FILES] == [f'{i:02d}' for i in range(1, 13)], [p.name for p in FILES]
doc = new_document()
for i, p in enumerate(FILES):
    spec = importlib.util.spec_from_file_location(p.stem.replace('-', '_'), p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    if i: doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    m.build(doc); print('  med:', p.name)
save(doc, 'all_tables')
print('Metod: samlingsdokument, samma innehåll som de enskilda filerna (se varje tabells not för inferens)')
