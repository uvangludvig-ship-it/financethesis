"""Plot frozen review components, without additional estimates or sample selection."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

O = Path(__file__).resolve().parent
d = pd.read_csv(O/'activity/REVIEW_COMPONENTS.csv')
x = np.arange(len(d))
fig, ax = plt.subplots(figsize=(9.2, 5.1))
ax.bar(x, d.day_EDminus1, .65, color='#3569a0', label='Handelsdagen')
ax.bar(x, d.other44, .65, bottom=d.day_EDminus1.where(d.other44>=0, 0),
       color='#c5814b', label='Övriga 44 dagar')
ax.scatter(x, d.total45, color='#20252b', s=30, label='Hela perioden', zorder=4)
ax.axhline(0, color='#777777', linewidth=.8)
ax.set_xticks(x, d.review.str.replace('H1', ' vår').str.replace('H2', ' höst'), rotation=35, ha='right')
ax.set_ylabel('Skillnad mot kontroller, i normala dagsomsättningar')
ax.set_title('Handelspiken och handeln runtomkring', loc='left', fontsize=14, pad=16)
ax.legend(frameon=False, ncol=3, loc='upper left')
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', alpha=.2)
fig.text(.12, .025, '65 tillägg, 10 översyner, samma tre jämförelseaktier per tillägg. Bruttohandel i SEK.\n'
         'Varje aktie normaliseras med sin egen tidigare dagsomsättning. Komponenter är beskrivande; inga separata test.', fontsize=8)
fig.tight_layout(rect=(0,.09,1,1))
fig.savefig(O/'TRADING_ACCOUNTING.png', dpi=180)
fig.savefig(O/'TRADING_ACCOUNTING.pdf')
