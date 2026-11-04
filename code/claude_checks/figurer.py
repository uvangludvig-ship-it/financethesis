# Created: 2026-11-04 17:43:19 CET (from date)
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
    fig, axes = plt.subplots(2, 1, figsize=(10.6, 7.2), sharex=True,
                             gridspec_kw={'height_ratios': [1.3, 1], 'hspace': 0.34})
    colors = ['#23658A', '#B15A36']
    x = d.ar.to_numpy()
    ax = axes[0]
    ax.set_title('A. Index funds’ net buying at index changes', loc='left', pad=30)
    for ty, sign, offset, color in [('addition', 1, -0.2, colors[0]), ('deletion', -1, 0.2, colors[1])]:
        y = sign*d['D_'+ty].to_numpy()
        ax.bar(x+offset, y, width=0.38, color=color)
        for year, height, n in zip(x+offset, y, d['n_'+ty]):
            if np.isfinite(height):
                ax.annotate(str(int(n)), (year, height), xytext=(0, sign*4),
                            textcoords='offset points', ha='center',
                            va='bottom' if sign > 0 else 'top', fontsize=7)
    ax.text(0, 1.04, 'Additions', color=colors[0], transform=ax.transAxes)
    ax.text(0.13, 1.04, 'Deletions', color=colors[1], transform=ax.transAxes)
    ax.text(1, 1.04, 'Bar labels: number of events', ha='right', transform=ax.transAxes, fontsize=9)
    ax.axhline(0, color='black', linewidth=0.6)
    ax.set_ylabel('Net buying (% of shares)')
    ax.margins(y=0.18)
    ax = axes[1]
    ax.plot(x, d.agarandel_pct, color='black', linewidth=1.5)
    ax.set_title('B. Index funds’ share of OMXSB market value', loc='left', pad=12)
    ax.set_ylabel('Share of OMXSB market value (%)')
    ax.set_ylim(bottom=0)
    ax.text(0.98, 0.65, 'Index funds', transform=ax.transAxes, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels([str(v) for v in x], rotation=45, ha='right')
    ax.set_xlim(x.min()-0.7, x.max()+0.7)
    ax.set_xlabel('Year')
    fig.suptitle("Figure 1. Index funds’ net buying at OMXSB changes and their share of the index, 2007–2026", fontsize=12, y=0.98)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.12, top=0.86)
    OUT.mkdir(parents=True, exist_ok=True)
    for suffix in ['png', 'pdf']:
        fig.savefig(OUT/f'figur1.{suffix}', dpi=300)
    plt.close(fig)
    caption = ("Figure 1. Index funds' net buying at OMXSB changes and their share of the index, 2007–2026. "
               "Panel A reports annual mean D for additions (positive bars) and deletions (negative bars); labels give the number of events in each mean. "
               "D is index funds’ net buying between the report before AD (announcement date) and the report after ED (effective date), as a percentage of the share class’s shares. "
               "Deletion D is sign-adjusted in the source and plotted with its sign reversed. Missing means are omitted. "
               "Panel B shows index funds’ assets divided by OMXSB members’ aggregate market value at the final review of the year, in percent. "
               "Source: LSEG Lipper and SHoF; authors’ calculations. "
               "The fund classification follows data/input/omxsb/tracker_mandates.csv; the figure is rerun when that file is final.\n")
    (OUT/'figur1.txt').write_text(caption)
    log = (f'Run: {timestamp} (date)\n{Path(__file__).read_text().splitlines()[0]}\n'
           f'Source: {SOURCE.relative_to(ROOT)}\nSHA256: {hashlib.sha256(SOURCE.read_bytes()).hexdigest()}\n'
           f'Font: {font}\nPNG: 300 dpi; PDF: embedded TrueType font.\n'
           'D_deletion multiplied by -1 for plotting; no imputation of missing means.\n'
           'PASS: ownership endpoints close to 0.06 and 1.3.\n' + d.to_string(index=False) + '\n')
    (OUT/'LOGG.txt').write_text(log)
    print(log)


if __name__ == '__main__':
    main()
