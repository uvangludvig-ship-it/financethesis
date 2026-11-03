"""One bounded primary-source identity repair. No price/return data read."""
from pathlib import Path
import pandas as pd,json,re,hashlib,datetime,shutil
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');D=O/'identity_sources'
manifest={x['file']:x for x in json.loads((D/'manifest.json').read_text())if x['status']=='downloaded'}
def evidence(ric,isin,files,date,basis):
 for file in files:assert file in manifest
 return dict(ric=ric,isin=isin,source_files=';'.join(files),source_urls=';'.join(manifest[x]['url']for x in files),evidence_date=date,basis=basis)
rows=[
 evidence('ABB.ST','CH0012221716',['abb_listing.html'],'2026-11-03 retrieval','Issuer explicitly pairs ordinary ISIN and Stockholm Reuters code; historical dated Nasdaq ordinary ISIN identical. ABB U is a different security and excluded.'),
 evidence('AZN.ST','GB0009895292',['bnp_2016.pdf'],'2016-02-02','Exchange-filed BNP underlying table explicitly pairs ordinary name, ISIN, SEK and Reuters code; same exact ISIN appears on dated Stockholm roster.'),
 evidence('ALIVsdb.ST','SE0000382335',['bnp_2016.pdf'],'2016-02-02','Exchange-filed BNP underlying table explicitly pairs Swedish depositary receipt ISIN, SEK and Reuters code. This is the dated Stockholm ordinary-equity exposure, not NYSE stock or a redemption line.'),
 evidence('INVEb.ST','SE0000107419',['bnp_2016.pdf','investor_split2021.pdf'],'2016-02-02;2021-05-18','Direct old ISIN/RIC in primary securities table; ICE confirms B-class split transition to currently verified static ISIN SE0015811963 on2021-05-19.'),
 evidence('ATCOa.ST','SE0011166610',['atlas_share.html','atlas_split2022.html'],'2022-05-10;2026-11-03 retrieval','Issuer identifies Reuters code for A class; Nasdaq maps old/new A-class ISIN and unchanged orderbook; new ISIN also verified in local LSEG static.'),
 evidence('ATCOb.ST','SE0011166628',['atlas_share.html','atlas_split2022.html'],'2022-05-10;2026-11-03 retrieval','Issuer identifies Reuters code for B class; Nasdaq maps old/new B-class ISIN and unchanged orderbook.'),
 evidence('ATCOb.ST','SE0017486897',['atlas_share.html','atlas_split2022.html'],'2022-05-10;2026-11-03 retrieval','Issuer code for B class and Nasdaq new B-class ISIN, effective2022-05-13.'),
 evidence('HEXAb.ST','SE0000103699',['hexagon_split2021.html'],'2021-05-10','Nasdaq unchanged B-class orderbook old/new ISIN; new ISIN SE0015961909 already exact-matched to local LSEG HEXAb.ST.'),
 evidence('ELUXb.ST','SE0000103814',['bnp_2016.pdf','electrolux_split2021.html'],'2016-02-02;2021-09-27','Primary table explicitly maps old ISIN/RIC; Nasdaq confirms unchanged B-class orderbook and successor static ISIN SE0016589188.'),
 evidence('BOL.ST','SE0011088665',['bnp_2016.pdf','boliden_split2018.html'],'2016-02-02;2018-05-11','Primary table maps BOL.ST to old ordinary ISIN SE0000869646; Nasdaq unchanged ordinary orderbook changes to SE0011088665 effective2018-05-16.'),
]
I=pd.DataFrame(rows)
# Require downloaded source assertions, not just remembered identifiers.
for s in ['AZN.ST','GB0009895292','ALIVsdb.ST','SE0000382335','INVEb.ST','SE0000107419','BOL.ST','SE0000869646','ELUXb.ST','SE0000103814']:
 assert s in (D/'bnp_2016.txt').read_text()
for s in ['ATCOa.ST','ATCOb.ST']:assert s in (D/'atlas_share.html').read_text()
for s in ['SE0011166610','SE0011166628','SE0017486889','SE0017486897']:assert s in (D/'atlas_split2022.html').read_text()
assert 'ABB.ST'in(D/'abb_listing.html').read_text()
U=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_pool/review_RIC_control_pool.csv')
RO=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv')
panelids=set(pd.read_csv(R/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv',usecols=['ric']).ric)
assert set(I.ric)<=panelids
assert 'NDASE.ST' not in panelids
RO['review']=RO.month.astype(str).str[:4]+RO.month.astype(str).str[4:].map({'04':'H1','10':'H2'})
ordinary=RO.stock_type&RO.listed_at_month_end&~RO.preference_name_flag&~(RO.instrument.fillna('')+' '+RO.ticker.fillna('')).str.contains(r'\b(?:U|PREF|PREFERENS|BTA|BTR|INL|IL|RTS|RIGHT|REDEMPTION|WARRANT)\b',case=False,regex=True)
added=[]
for x in I.itertuples():
 for r in RO[ordinary&RO['isin'].eq(x.isin)&RO.month.between(201904,202510)].itertuples():
  if ((U.review==r.review)&(U.ric==x.ric)).any():
   assert U.loc[(U.review==r.review)&(U.ric==x.ric),'isin'].eq(x.isin).all();continue
  assert not((U.review==r.review)&(U['isin']==x.isin)).any(),'Do not overwrite quote alternatives'
  d={k:getattr(r,k,None)for k in U.columns};d.update(ric=x.ric,nasdaq_isin=x.isin,isin=x.isin,issuer_key=r.review+':'+r.company_code,evidence_type='primary_source_identity_completion_20261103',evidence_source=x.source_urls,same_instrument_RIC_count=1,same_instrument_RIC_alternatives=x.ric)
  added.append(d)
A=pd.DataFrame(added);V=pd.concat([U,A],ignore_index=True);assert not V.duplicated(['review','ric']).any()
V.to_csv(O/'completed_review_RIC_pool.csv',index=False);A.to_csv(O/'added_review_identity_rows.csv',index=False);I.to_csv(O/'completed_identity_evidence.csv',index=False)
# Preserve the original lock and source script. The rerun differs only by one
# input pool and an explicit U exclusion, recorded in the amendment.
Z=O/'repair_round';Z.mkdir(exist_ok=True)
for name in ['DESIGN_LOCK.json','IDENTITY_COMPLETION_AMENDMENT.json']:shutil.copy2(O/name,Z/name)
code=(O/'design_and_gate.py').read_text().replace("'pool':R/'output/omxsb_open_questions_20261102/eligible_pool/review_RIC_control_pool.csv'","'pool':Path("+repr(str(O/'completed_review_RIC_pool.csv'))+")")
code=code.replace('(?:PREF|PREFERENS|BTA|BTR|INL|IL|RTS|RIGHT|REDEMPTION|WARRANT)','(?:U|PREF|PREFERENS|BTA|BTR|INL|IL|RTS|RIGHT|REDEMPTION|WARRANT)')
(Z/'design_and_gate.py').write_text(code)
audit=(O/'audit_gate.py').read_text().replace('assert not E.baseline_pass.any()',"assert not json.loads((O/'BASELINE_GATE.json').read_text())['gate_pass']")
(Z/'audit_gate.py').write_text(audit)
summary=dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),identity_pairs_added=len(I),new_review_rows=len(A),RICs=sorted(I.ric.unique()),no_return_columns_read=True,Nordea_Stockholm_RIC_absent=True,first_gate_preserved='first_gate/',thresholds_weights_targets_controls_unchanged=True,transient_U_exclusion_added=True,files={str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [O/'completed_review_RIC_pool.csv',O/'completed_identity_evidence.csv',Z/'design_and_gate.py']})
(O/'IDENTITY_COMPLETION.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
