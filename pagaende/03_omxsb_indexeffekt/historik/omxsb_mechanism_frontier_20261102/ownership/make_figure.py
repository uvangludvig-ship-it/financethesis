from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import t
O=Path(__file__).resolve().parent
D=pd.read_csv(O/"decomp_event_groups.csv");A=D[D.type=="addition"].pivot(index=["event_id","review"],columns="group",values="matched_change")
A["family"]=A.OMXSB_index_named+A.OMXSB_other_named;A["rest"]=A.ALL-A.family
Y=A.groupby("review").mean();G=len(Y);metrics=["ALL","family","rest"];values=Y[metrics].mean();err=t.ppf(.975,G-1)*Y[metrics].std(ddof=1)/np.sqrt(G)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.spines.top":False,"axes.spines.right":False})
fig,ax=plt.subplots(figsize=(9,5.4));fig.subplots_adjust(left=.38,right=.95,top=.76,bottom=.31)
y=np.arange(3);ax.barh(y,values,color=["#245675","#247c7a","#8998a4"],height=.52);ax.errorbar(values,y,xerr=err,fmt="none",ecolor="#182c3b",capsize=4,lw=1.5)
ax.set_yticks(y,["Alla inkluderade fonder","Fonder med OMXSB\ni jämförelseindexet","Övriga inkluderade fonder"]);ax.invert_yaxis();ax.set_xlim(-.6,14.1);ax.set_xticks([0,2,4,6,8,10,12,14]);ax.axvline(0,color="#333",lw=.6);ax.spines["left"].set_visible(False);ax.grid(axis="x",alpha=.18);ax.set_axisbelow(True);ax.set_xlabel("Extra fondägare jämfört med kontrollaktierna")
for yi,v in zip(y,values):ax.text(v-.15,yi-.12,f"{v:.1f}".replace(".",","),color="white",ha="right",va="center",weight="bold")
fig.text(.055,.93,"Ägarökningen är koncentrerad till OMXSB-mandat",fontsize=16,weight="bold");fig.text(.055,.86,"8,5 av 9,9 extra fondägare finns i OMXSB-relaterade mandat.",fontsize=12)
fig.text(.055,.085,"118 tillägg 2019–2025. Tre fasta huvudlistekontroller per händelse.\nLika vikt per översyn (14 översyner); 95%-intervall. Kvartalsägande, inte affärer på indexdagen.",fontsize=9,color="#394a56")
fig.savefig(O/"ownership_concentration.png",dpi=180);fig.savefig(O/"ownership_concentration.pdf");plt.close(fig)
