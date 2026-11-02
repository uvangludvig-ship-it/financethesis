from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

W=Path(__file__).resolve().parent
OUT=W.parents[1]/'outputs'
# W is .../work/open_questions_20261101; outputs is the task's sibling of work.
OUT.mkdir(exist_ok=True)
r=pd.read_csv(W/'eligible_rematch/results.csv')
s=r[(r.type=='addition')&(r.support=='common100')].set_index('contrast')
h=np.array([1,20,60,100]);q=s.loc[[f'level_{x}' for x in h]]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(10,6.5),facecolor='white')
fig.subplots_adjust(top=.76,bottom=.29,left=.12,right=.96)
fig.text(.12,.94,'Tydligt försprång först, osäkrare senare',fontsize=22,weight='bold',color='#163447')
fig.text(.12,.885,'Samma 135 tillägg • Tre daterat verifierade huvudlistekontroller per tillägg',fontsize=12,color='#44545f')
fig.text(.12,.835,'Explorativ analys. Avkastning relativt kontrollerna, inte aktiernas absoluta kursfall.',fontsize=10,color='#44545f')
ax.axhline(0,color='#a9b3b9',lw=1)
ax.plot(h,q.estimate_pp,color='#126b7d',lw=2.4,zorder=3)
ax.errorbar(h,q.estimate_pp,yerr=np.vstack([q.estimate_pp-q.ci_lo,q.ci_hi-q.estimate_pp]),fmt='o',ms=7,color='#126b7d',ecolor='#6ca7b0',capsize=6,elinewidth=2,zorder=4)
for x,y in zip(h,q.estimate_pp):ax.text(x,y+.35,f'{y:+.2f}'.replace('.',','),ha='center',fontsize=11,color='#163447',weight='bold')
ax.set_xticks(h,['1','20','60','100']);ax.set_xlabel('Handelsdagar efter indexändringen',labelpad=10)
ax.set_ylabel('Ackumulerat avkastningsförsprång\n(procentenheter)',labelpad=12)
ax.set_ylim(-7,6);ax.set_xlim(-5,106);ax.grid(axis='y',color='#e8edef',lw=.7)
fig.text(.12,.12,'Förändring dag 20 → 100: −4,01 procentenheter (95 % intervall −8,47 till +0,46).',fontsize=11,weight='bold',color='#163447')
fig.text(.12,.065,'Staplar: punktvisa 95 % intervall. Lika vikt över 19 översyner. Alla matchningar väljs före utfall.\nOfullständig panellänkning, bortfall och kvarvarande urval begränsar tolkningen; orsaken identifieras inte.',fontsize=9,color='#52616a')
fig.savefig(OUT/'OMXSB_sen_forandring_20261101.png',dpi=180)
fig.savefig(OUT/'OMXSB_sen_forandring_20261101.pdf')
print(OUT/'OMXSB_sen_forandring_20261101.png')
