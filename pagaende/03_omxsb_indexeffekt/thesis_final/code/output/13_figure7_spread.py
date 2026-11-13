# Figur 7 (G&S Figure 9): värdeviktad relativ noterad spread per år, OMXSB-bolagen och alla aktier i panelen.
# Ur results/liquidity/spread_by_year.csv (steg 11). Lutningen i noten ur results/liquidity/liquidity_results.csv (samma steg).
# Kontroll: årets CAR och antal i spread-filen = results/effect/effect_by_year.csv (01), och spreaden 2007 och 2025 i båda filerna.
# Körs från thesis_final efter 11: python3 code/output/13_figure7_spread.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

STEM = Path(__file__).stem
S = pd.read_csv(RES / 'liquidity' / 'spread_by_year.csv')
L = pd.read_csv(RES / 'liquidity' / 'liquidity_results.csv')
Y = pd.read_csv(RES / 'effect' / 'effect_by_year.csv', header=[0, 1], index_col=0)
Y = Y.loc[[i for i in Y.index if str(i).isdigit()]]; Y.index = Y.index.astype(int)
assert list(S.year) == list(range(2007, 2027)) and list(Y.index) == list(S.year)
for pre, t in [('Additions', 'addition'), ('Deletions', 'deletion')]:
    assert np.allclose(S[f'{t}_effect_mean'], Y[(pre, 'Total')].astype(float), equal_nan=True), t
    assert (S[f'N_{t}s'].values == Y[(pre, 'N')].astype(int).values).all(), t
for y in [2007, 2011, 2016, 2021, 2025, 2026]:
    assert abs(one(L, test='A spread', rad=f'värdeviktad spread {y} (%)').b - one(S, year=y).vw_spread_omxsb_members) < 1e-12
SL = {t: one(L, test='A spread', typ=t, urval='tabell 1') for t in ['addition', 'deletion']}


def png():
    plt = fig_setup(); fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for c, col, lab in [('vw_spread_all_st_panel', THIRD, 'All stocks on the main market'), ('vw_spread_omxsb_members', ADD, 'OMXSB members')]:
        ax.plot(S.year, S[c], color=col, lw=2, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.8, label=lab)
    ax.set_ylim(0, None); ax.set_xticks(range(2007, 2027, 2))
    ax.set_ylabel('Value-weighted quoted spread (% of price)')
    ax.legend(loc='upper right', fontsize=8)
    p = OUT / f'{STEM}.png'; OUT.mkdir(parents=True, exist_ok=True); fig.savefig(p); plt.close(fig); return p


def build(doc):
    title(doc, 'fig_spread', 'Bid-ask spreads, by year')
    figure(doc, png())
    a, d = SL['addition'], SL['deletion']
    # utkast: författarna formulerar om noten
    note(doc, 'Value-weighted average relative quoted spread, (ask − bid) / midpoint at the close in per cent, by calendar year, for '
         'OMXSB members and for all stocks in the price panel of the Nasdaq Stockholm main market (on average '
         f'{int(S.n_panel_stocks_with_quote.min())} to {int(S.n_panel_stocks_with_quote.max())} stocks with a quote). Observations '
         'above 20 per cent are dropped. Greenwood and Sammon (2025, Figure 9) use the effective spread and the implementation '
         'shortfall of index funds; we have only closing quotes. Regressing the total-window CAR of each event on the OMXSB '
         f'spread in its year gives a slope of {num(a.b)}{stars(a.p_wcb)} {ci(a.lo, a.hi)} for additions ({int(a.n)} events) and '
         f'{num(d.b)}{stars(d.p_wcb)} {ci(d.lo, d.hi)} for deletions ({int(d.n)} events), in percentage points of CAR per '
         f'percentage point of spread. Inference for the slopes: {WCR}; brackets are {WCR_CI}; stars from the same draws: '
         f'{STARS}.')


if __name__ == '__main__':
    run(build, STEM)
    print('Metod: figuren beskrivande; lutningarna i noten = wild cluster bootstrap per översyn (intervall genom testinversion)')
