from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R=next(p for p in Path(__file__).resolve().parents if (p/'data/raw/lseg').is_dir())
W=R/'output/omxsb_followup_20261102'
O=W/'figures';O.mkdir(exist_ok=True)
a=pd.read_csv(W/'owner_concentration_stability_20261102/all_omissions.csv')
a=a[a.type.eq('addition') & a.omitted.isin(['none','nordea funds ab'])].set_index('omitted').loc[['none','nordea funds ab']]
r=pd.read_csv(W/'retention_scaling_feasibility_20261102/relative_retention_summary.csv').set_index('fund')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,(ax,bx)=plt.subplots(1,2,figsize=(12,5.8),gridspec_kw={'width_ratios':[1.1,1]})
fig.suptitle('Ägarförändringen består efter två extra kontroller',fontsize=17,fontweight='bold',x=.06,ha='left',y=.98)
ax.set_title('1. Resultatet hänger inte bara på Nordea',loc='left',fontsize=12,pad=18)
ax.bar([0,1],a.family,color='#225f79',width=.56,label='OMXSB-relaterade mandat')
ax.bar([0,1],a.total-a.family,bottom=a.family,color='#c8d5da',width=.56,label='Övriga observerade fonder')
for i,(_,x) in enumerate(a.iterrows()):
    ax.text(i,x.family/2,f'{100*x.ratio:.0f} %',ha='center',va='center',color='white',fontsize=18,fontweight='bold')
    ax.text(i,x.total+.18,f'+{x.total:.2f}'.replace('.',','),ha='center',fontsize=12)
ax.set_xticks([0,1],['Hela fondurvalet','Utan Nordea Funds Ab'])
ax.set_ylabel('Extra fondägare efter tillägg, jämfört med kontroller')
ax.set_ylim(0,12);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.07),frameon=False,fontsize=9)
ax.text(0,1.01,'Punktestimat • 118 tillägg • 14 översyner',transform=ax.transAxes,fontsize=9,color='#555')
bx.axis('off');bx.set_title('2. Nya positioner behålls relativt övriga innehav',loc='left',fontsize=12,pad=18)
bx.text(0,.88,'Median relativ positionsstorlek vid nästa rapport',fontsize=10,color='#555',transform=bx.transAxes)
for y,name in [(.65,'Nordea'),(.38,'Nordnet')]:
    x=r.loc[name]
    bx.text(0,y,name,fontsize=13,transform=bx.transAxes)
    bx.text(.78,y,f'{100*x.median_relative_ratio:.1f} %'.replace('.',','),ha='right',fontsize=24,fontweight='bold',color='#225f79',transform=bx.transAxes)
    bx.text(0,y-.09,f'{int(x.defined_N)} positiva startpositioner',fontsize=10,color='#555',transform=bx.transAxes)
bx.text(0,.12,'100 % = samma proportionella antalstillväxt\nsom fondens förhandsvalda referenskorg.',fontsize=10,transform=bx.transAxes,linespacing=1.5)
fig.text(.06,.035,'Källor: FI och daterade Nasdaq-listor. Explorativa kontroller. Kvartalsinnehav är inte dagsaffärer; resultaten förklarar inte prisreaktionen.',fontsize=9,color='#555')
fig.subplots_adjust(top=.81,bottom=.2,left=.07,right=.98,wspace=.35)
fig.savefig(O/'OMXSB_tva_agarresultat_20261102.png',dpi=180)
fig.savefig(O/'OMXSB_tva_agarresultat_20261102.pdf')
