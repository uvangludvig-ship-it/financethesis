# Figur 6 (G&S Figure 8): tilläggens rang bland aktier utanför OMXSB, per år, efter börsvärde och efter omsättning.
# Ur results/liquidity/size_rank_by_year.csv (steg 11). Vänster: rang (1 = störst), höger: percentil (rang / antal aktier).
# Kontroll: årsmedlen räknas om ur results/liquidity/size_rank_of_additions.csv (en rad per tillägg, samma steg).
# Körs från thesis_final efter 11: python3 code/output/10_figure6_size_rank.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

STEM = Path(__file__).stem
Y = pd.read_csv(RES / 'liquidity' / 'size_rank_by_year.csv')
E = pd.read_csv(RES / 'liquidity' / 'size_rank_of_additions.csv')
assert list(Y.year) == list(range(2007, 2027))
for col, src in [('mean_mcap', 'rank_mcap'), ('mean_turn', 'rank_turnover'), ('pct_mcap_mean', 'pct_mcap'), ('pct_turn_mean', 'pct_turnover')]:
    m = E.groupby('year')[src].mean().reindex(Y.year).values
    assert np.allclose(m, Y[col].values, equal_nan=True), col
SER = [('mcap', ADD, 'Market value'), ('turn', THIRD, 'Turnover')]


def png():
    plt = fig_setup(); fig, axs = plt.subplots(1, 2, figsize=(6.5, 3.2), sharex=True)
    for ax, (pre, lab) in zip(axs, [('mean_', 'Mean rank (1 = largest)'), ('pct_', 'Mean percentile (1 = largest)')]):
        for k, col, l in SER:
            c = f'mean_{k}' if pre == 'mean_' else f'pct_{k}_mean'
            ax.plot(Y.year, Y[c], color=col, lw=2, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.8, label=l)
        ax.set_title(lab, fontsize=9, loc='left'); ax.set_ylim(0, None); ax.set_xticks(range(2007, 2027, 4))
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, [f'Ranked by {x.lower()}' for x in l], loc='lower center', ncol=2, fontsize=8)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    p = OUT / f'{STEM}.png'; OUT.mkdir(parents=True, exist_ok=True); fig.savefig(p); plt.close(fig); return p


def build(doc):
    title(doc, 'fig_size_rank', 'Rank of additions among stocks outside the OMXSB index, by year')
    figure(doc, png())
    # utkast: författarna formulerar om noten
    note(doc, 'For each addition we rank all stocks on the Nasdaq Stockholm main market that are not OMXSB members on the last '
         'trading day of the month before the announcement, by market value (the variable in Greenwood and Sammon, 2025, '
         'Figure 8) and by turnover over the previous six months (the variable Nasdaq uses to select OMXSB members). Rank 1 is the '
         'largest stock. Left: mean rank by year of the effective date; right: the same rank divided by the number of ranked '
         'stocks, in per cent, since the number of listed stocks roughly doubles over the sample '
         f'({int(Y.universe.min())} to {int(Y.universe.max())} stocks). {int(Y.N.sum())} additions, of which '
         f'{int(Y.N_ranked.sum())} could be ranked. Market value from LSEG for the whole company. Descriptive; no inference.')


if __name__ == '__main__':
    run(build, STEM)
    print('Metod: beskrivande (medel per år), ingen inferens')
