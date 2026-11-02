import os
from pathlib import Path
import pandas as pd,re,json
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO', str(Path(__file__).resolve().parents[3])));B=R/'output/omxsb_open_questions_20261102'
S=pd.read_csv(O/'security_role_gate.csv');G=pd.read_csv(O/'H_fund_review_gate.csv',dtype={'fund_id':str});H=pd.read_csv(O/'selected_full_fund_reports.csv.gz',dtype={'fund_id':str});U=pd.read_csv(B/'eligibility/dated_stockholm_instrument_roster.csv')
known=U.groupby('company_code')['isin'].agg(set).to_dict()
def norm(x):return re.sub(r'[^a-z0-9]','',str(x).lower().replace('å','a').replace('ä','a').replace('ö','o'))
H['name_norm']=H['name'].map(norm)
checks=[]
for (rev,ric),sg in S.groupby(['review','ric']):
 s=sg.iloc[0];ids=set(s.aliases.split(';'));others=known.get(s.company_code,set())-ids
 # Primary Nasdaq issuer name start is a screening hint only, not an accepted identity mapping.
 first=re.split(r'\s+',str(s.instrument))[0];token=norm(first)
 if len(token)<3:continue
 fs=set(G.loc[(G.review==rev)&G.eligible,'fund_id']);qs=[s.qminus,s.q0,s.q1]
 rows=H[H.fund_id.isin(fs)&H.quarter.isin(qs)&H.name_norm.str.startswith(token)&~H['isin'].isin(ids)]
 for h in rows.itertuples():
  status='known_other_listed_class'if h.isin in others else ('non_ordinary_container'if not h.ordinary_container else 'unresolved')
  checks.append(dict(review=rev,ric=ric,target=s.instrument,target_isin=s.nasdaq_isin,fund_id=h.fund_id,quarter=h.quarter,instrument=h.name,isin=h.isin,quantity=h.qty,value=h.value,asset_type=h.asset_type,status=status))
D=pd.DataFrame(checks).drop_duplicates();D.to_csv(O/'same_issuer_identity_screen.csv',index=False)
print(D.groupby('status').size().to_string());print(D[D.status=='unresolved'][['ric','target','instrument','isin','asset_type']].drop_duplicates().to_string(index=False))
