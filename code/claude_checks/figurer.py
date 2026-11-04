# Updated: 2026-11-04 17:53:40 CET (from date)
"""Generate Figure 1 exclusively from G_figur1_figur5.csv; no Word launch."""
from pathlib import Path
import hashlib
import subprocess
import os
import tempfile

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'financethesis-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'code/claude_checks/runda11_resultat/G_figur1_figur5.csv'
OUT = ROOT / 'output/figurer'


def main():
    timestamp = subprocess.check_output(['date', '+%Y-%m-%d %H:%M:%S %Z'], text=True).strip()
    d = pd.read_csv(SOURCE).sort_values('ar')
    assert d.ar.is_unique
    assert abs(d.iloc[0].agarandel_pct - 0.06) < 0.01
    assert d.loc[d.ar.isin([2025, 2026]), 'agarandel_pct'].between(1.2, 1.4).all()
    assert d[['D_addition', 'D_deletion']].min().min() >= 0
    for ty in ['addition', 'deletion']:
        assert d.loc[d['D_'+ty].isna(), 'n_'+ty].eq(0).all()
    font = font_manager.findfont('Times New Roman', fallback_to_default=False)
    plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 10,
                         'pdf.fonttype': 42, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.grid': False})
    fig, axes = plt.subplots(2, 1, figsize=(10.6, 8.0), sharex=True,
                             gridspec_kw={'height_ratios': [1.3, 1], 'hspace': 0.60})
    colors = ['#23658A', '#B15A36']
    x = d.ar.to_numpy()
    ax = axes[0]
    ax.set_title('A. Net purchases around OMXSB additions and deletions', loc='left', pad=59, fontweight='bold')
    ax.text(0, 1.19, 'Annual mean per event. Positive = net buying; negative = net selling.', transform=ax.transAxes)
    for ty, sign, offset, color in [('addition', 1, -0.2, colors[0]), ('deletion', -1, 0.2, colors[1])]:
        y = sign*d['D_'+ty].to_numpy()
        label = 'Stocks added to OMXSB' if ty == 'addition' else 'Stocks deleted from OMXSB'
        ax.bar(x+offset, y, width=0.38, color=color, label=label)
        for year, height, n in zip(x+offset, y, d['n_'+ty]):
            if np.isfinite(height):
                ax.annotate(str(int(n)), (year, height), xytext=(0, sign*4),
                            textcoords='offset points', ha='center',
                            va='bottom' if sign > 0 else 'top', fontsize=7)
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.035), ncol=2,
              frameon=False, borderaxespad=0, handlelength=1.3, columnspacing=2)
    ax.axhline(0, color='black', linewidth=0.6)
    ax.set_ylabel('Net purchases (% of share-class shares)')
    ax.margins(y=0.18)
    ax.text(0, -0.13, 'Small numbers give the number of events behind each bar.',
            transform=ax.transAxes, fontsize=9, color='#444444')
    ax = axes[1]
    ax.plot(x, d.agarandel_pct, color='black', linewidth=1.5)
    ax.set_title('B. OMXSB index fund assets relative to the index', loc='left', pad=34, fontweight='bold')
    ax.text(0, 1.06, 'Index fund assets divided by OMXSB market value — a measure of funds’ relative size.',
            transform=ax.transAxes)
    ax.set_ylabel('Fund assets / OMXSB market value (%)')
    ax.set_ylim(bottom=0)
    ax.set_xticks(x)
    ax.set_xticklabels([str(v) for v in x], rotation=45, ha='right')
    ax.set_xlim(x.min()-0.7, x.max()+0.7)
    ax.set_xlabel('Year')
    fig.suptitle('Figure 1. OMXSB index funds: trading at index changes and relative size, 2007–2026', fontsize=12, y=0.98)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.11, top=0.80)
    OUT.mkdir(parents=True, exist_ok=True)
    for suffix in ['png', 'pdf']:
        fig.savefig(OUT/f'figur1.{suffix}', dpi=300)
    plt.close(fig)
    caption = ("Figure 1. OMXSB index funds: trading at index changes and relative size, 2007–2026. "
               "Panel A reports annual mean D for additions (positive bars) and deletions (negative bars); labels give the number of events in each mean. "
               "D is index funds’ net buying between the report before AD (announcement date) and the report after ED (effective date), as a percentage of the share class’s shares. "
               "Deletion D is sign-adjusted in the source and plotted with its sign reversed. Missing means are omitted. "
               "Panel B shows index funds’ assets divided by OMXSB members’ aggregate market value at the final review of the year, in percent. "
               "This aggregate asset ratio measures the funds’ relative size; it is not a direct measurement of their holdings in every index constituent. "
               "Source: LSEG Lipper and SHoF; authors’ calculations. "
               "The fund classification follows data/input/omxsb/tracker_mandates.csv; the figure is rerun when that file is final.\n")
    (OUT/'figur1.txt').write_text(caption)
    log = (f'Run: {timestamp} (date)\n{Path(__file__).read_text().splitlines()[0]}\n'
           f'Source: {SOURCE.relative_to(ROOT)}\nSHA256: {hashlib.sha256(SOURCE.read_bytes()).hexdigest()}\n'
           f'Font: {font}\nPNG: 300 dpi; PDF: embedded TrueType font.\n'
           'D_deletion multiplied by -1 for plotting; no imputation of missing means.\n'
           'Presentation: keyed legend; explicit purchasing/selling interpretation; Panel B identified as an asset ratio; no floating line label.\n'
           'PASS: ownership endpoints close to 0.06 and 1.3.\n' + d.to_string(index=False) + '\n')
    (OUT/'LOGG.txt').write_text(log)
    print(log)


if __name__ == '__main__':
    main()
