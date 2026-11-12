# Tabell 13: tvillingar, spreaden mellan indexslaget och systerslaget i samma bolag. Placeboinferens.
# Ur results/twins/twin_results_summary.csv och ab_revision_results.csv (steg 16). Kontroll: jämförelsen med körningen 1–2 nov
# i results/twins/TWINS.md utan avvikelser, och tillägg + borttag = alla i revisionen.
# Körs från thesis_final efter 16: python3 code/output/21_table13_twins.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

S = pd.read_csv(RES / 'twins' / 'twin_results_summary.csv')
A = pd.read_csv(RES / 'twins' / 'ab_revision_results.csv')
assert 'Avvikelser' not in (RES / 'twins' / 'TWINS.md').read_text(encoding='utf-8')
assert one(A, urval='tillägg').N + one(A, urval='borttag').N == one(A, urval='alla rensade').N
WIN = [('primär [AD-1,ED+1]', 'Primary [AD−1, ED+1]'), ('medprimär återgång [ED,ED+20]', 'Reversal [ED, ED+20]'),
       ('sek [AD-1,AD+1]', 'Announcement [AD−1, AD+1]'), ('sek [AD+2,ED-2]', 'Between [AD+2, ED−2]'), ('sek [ED-1,ED+1]', 'Effective [ED−1, ED+1]'),
       ('placebo [AD-60,AD-21]', 'Placebo [AD−60, AD−21]'), ('placebo [AD-20,AD-2]', 'Placebo [AD−20, AD−2]')]
AB = [('alla rensade', 'All'), ('tillägg', 'Additions'), ('borttag', 'Deletions'), ('utan källbyte (bara panelens totalavkastning)', 'Total-return series only')]


def build(doc):
    title(doc, 'tab_twins', 'Twin share classes: the index class against its sister class')
    subhead(doc, 'Panel A. Spread by window')
    rows = []
    for k, lab in WIN:
        r = one(S, fönster=k)
        rows.append([lab, num(r.medel_händelse), num(r.p_händelse, 3), num(r.p_holm, 3) if pd.notna(r.p_holm) else '', num(r.medel_bolag), num(r.p_bolag, 3)])
    n0 = one(S, fönster=WIN[0][0])
    table(doc, ['', 'Mean (%)', 'p', 'p (Holm)', 'Mean by firm', 'p'], rows, [5.4, 2.3, 2.0, 2.0, 2.6, 2.0])
    subhead(doc, 'Panel B. Primary window after the revision of the price series')
    rows, cis = [], []
    for k, lab in AB:
        r = one(A, urval=k)
        rows.append([lab, num(r.skattning), ci(r.ci_lo, r.ci_hi), num(r.p, 3), str(int(r.N)), str(int(r.bolag))])
    table(doc, ['', 'Mean (%)', '95 % interval', 'p', 'Events', 'Firms'], rows, [5.4, 2.3, 3.4, 1.8, 1.8, 1.6])
    # utkast: författarna formulerar om noten
    note(doc, 'For index changes where one share class of a firm enters or leaves the OMXSB while its sister class does not, the '
         'spread is the log return of the index class minus that of the sister class over the window, in per cent, with the sign '
         f'reversed for deletions ({int(n0.N)} events in {int(n0.bolag)} firms). Inference: for each event, placebo windows '
         'of the same length start at the same time of year (±45 days) in other years, away from the firm\'s own index changes; '
         '5,000 draws of one placebo window per event give the null distribution of the mean. p (Holm): adjusted for the three '
         'secondary windows. Mean by firm: events averaged within firm first. Panel B repeats the primary window after a revision '
         'decided before it was run: prices instead of total returns where one leg comes from a separate LSEG download, and events '
         'with spikes, jumps or a stale sister class dropped (none were); brackets are percentile intervals from the placebo distribution.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: placebofördelning (5 000 dragningar), Holm för de sekundära fönstren')
