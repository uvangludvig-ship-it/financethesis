"""Locked AP/FI half-year ownership analysis; no prices/returns estimated.
Run prepare first. Original inputs and prior analyses are never modified.
"""
from pathlib import Path
import argparse, json, re, math, hashlib
import numpy as np
import pandas as pd
from scipy.stats import t
from omxsb_ap_prepare import norm

P=argparse.ArgumentParser();P.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]);P.add_argument('--out',type=Path);ARGS=P.parse_args()
ROOT=ARGS.repo;OUT=ARGS.out or ROOT/'output/omxsb_extension_20261031/ownership';OUT.mkdir(parents=True,exist_ok=True)
EVENTS=pd.read_csv(OUT/'events_locked.csv',parse_dates=['AD','ED','before','after','prior'])
EVENTS=EVENTS[EVENTS.main_period].copy()
META=pd.read_csv(OUT/'fi_fund_quarter_metadata.csv',parse_dates=['Kvartalsslut'])
H=pd.read_csv(OUT/'fi_halfyear_instrument_rows.csv.gz',parse_dates=['Kvartalsslut'])
BADH=pd.read_csv(OUT/'fi_halfyear_ambiguous_quantity_rows.csv',parse_dates=['Kvartalsslut'])
SN=pd.read_csv(OUT/'security_halfyear_snapshots.csv',parse_dates=['date','shares_date','close_date']).set_index(['RIC','date'])
CA=pd.read_csv(OUT/'halfyear_CA_review.csv',parse_dates=['before','after']).set_index(['event_id','window'])
AP=pd.read_csv(ROOT/'data/derived/ap/ap_svenska_aktier_med_ric.csv',parse_dates=['datum'])
EX=pd.read_csv(ROOT/'data/derived/ap/excluded_rows.csv',parse_dates=['datum'])
# Full original published Swedish portfolios, including otherwise removed foreign-domicile shares.
AP=pd.concat([AP,EX],ignore_index=True).fillna({'RIC':'','ISIN':'','RIC_kandidater':'','bolagsnamn':'','excluded':'','kallticker':''})
AP=AP[AP.fond.isin(['AP2','AP3','AP4'])].copy()
CHECK=pd.read_csv(ROOT/'data/derived/ap/source_checks.csv',parse_dates=['datum'])
ISINS={r:set(v) for r,v in json.load(open(OUT/'allowed_isins.json')).items()}
# Explicit class correction. Issuer identity alone cannot validate a share class.
REMOVE={'NCCb.ST':{'SE0000118952'},'STEr.ST':{'FI0009007603','FI0009005953','FI0009005961'},'KARO.ST^K22':{'SE0017767148'}}
for r,v in REMOVE.items():
 if r in ISINS:ISINS[r]-=v
UNRESOLVED_CLASS={'EMBRACb.ST'} # conflicting A/B labels; preserve exclusion until independent class source audit.
BEHAVIORAL=set(pd.read_csv(ROOT/'output/omxsb_audit_20261031/corrected/index_funds.csv').iloc[:,0].astype(int))
assert 60320 in BEHAVIORAL and 60293 in BEHAVIORAL
# Explicit public corporate actions, independently reviewed BEFORE new ownership changes.
ACTIONS=[
 ('LAGRb.ST','2020-10-07',3.,'ordinary_split','https://www.lagercrantz.com/media/press-archive/2020/change-in-number-of-shares-and-votes-in-lagercrantz-group-ab/'),
 ('ANODb.ST','2022-05-17',4.,'ordinary_split','https://www.addnodegroup.com/release/share-split-in-addnode-group/'),
 ('HEBAb.ST','2022-05-18',2.,'ordinary_split','https://ir.hebafast.se/aktien/'),
 ('FNOX.ST^G25','2022-01-19',10.,'ordinary_split','https://news.cision.com/se/fortnox-ab/r/fortnox-offentliggor-tidplan-for-aktiesplit,c3484089'),
 ('LIFCOb.ST','2021-05-06',5.,'ordinary_split','https://news.cision.com/lifco-ab/r/year-end-report-2021,c3496929'),
 ('HTRO.ST','2022-06-02',5.,'ordinary_split','https://www.globenewswire.com/news-release/2022/05/30/2452336/0/en/Hexatronic-Group-AB-publ-executes-share-split-and-decides-on-record-date.html'),
 ('BIOGb.ST','2022-05-18',5.,'ordinary_split','https://www.nasdaq.com/press-release/split-and-change-of-isin-for-biogaia-ab-72-22-2022-05-13'),
 ('PEABb.ST','2020-12-08',1.,'distribution_unchanged_ordinary_units','https://www.peab.com/financial-info/financial-summary/distribution-annehem/'),
 ('TETY.ST^A25','2019-06-01',1.,'redemption_distinct_ISIN_ordinary_units_unchanged','https://www.tethysoil.com/en/wp-content/uploads/sites/2/2020/03/tety-ar2019-eng.pdf'),
 ('TETY.ST^A25','2022-06-01',1.,'redemption_distinct_ISIN_ordinary_units_unchanged','https://www.tethysoil.com/en/wp-content/uploads/sites/2/2022/04/agm-2022-15-eng.pdf'),
 ('BETSb.ST','2021-06-07',1.,'redemption_distinct_ISIN_ordinary_units_unchanged','https://www.betssonab.com/sites/default/files/pr/202105054773-1.pdf'),
 ('BETSb.ST','2024-06-01',1.,'redemption_distinct_ISIN_ordinary_units_unchanged','https://www.betssonab.com/sites/default/files/pr/202504032329-1.pdf?ts=1743753776'),
 ('KINVb.ST','2024-06-07',1.,'redemption_distinct_ISIN_ordinary_units_unchanged','https://www.kinnevik.com/files/globalassets/documents/4.-governance/general-meetings/2024/Informationsbroschyr_2024_E.pdf'),
 ('SHOTE.ST','2020-06-01',1.,'rights_issue_ordinary_units_unchanged','https://www.scandichotelsgroup.com/media/press-releases/2020/scandic-announces-the-final-terms-of-its-fully-underwritten-rights-issue/'),
 ('CTEK.ST','2023-03-08',1.,'rights_issue_ordinary_units_unchanged','https://ctekgroup.com/en/investors/rights-issue/')]
ACTIONS=pd.DataFrame(ACTIONS,columns=['RIC','action_date','factor','kind','source']);ACTIONS.action_date=pd.to_datetime(ACTIONS.action_date);ACTIONS['date_precision']='source_dated_action_or_record_date';ACTIONS.loc[(ACTIONS.RIC.eq('TETY.ST^A25')&ACTIONS.action_date.eq('2019-06-01'))|(ACTIONS.RIC.eq('BETSb.ST')&ACTIONS.action_date.eq('2024-06-01')),'date_precision']='halfyear_window_locator_not_verified_exact_exdate';ACTIONS.loc[ACTIONS.RIC.eq('LIFCOb.ST'),'date_precision']='month_window_locator_source_confirms_May2021_not_exact_day';ACTIONS.to_csv(OUT/'corporate_action_sources.csv',index=False)
# An action_date may locate an event within its half-year, rather than claim an exact ex date.
DENOMS={('BETSb.ST','2023-12-31'):(121374972,'B total121571405 less treasury196433'),('BETSb.ST','2024-12-31'):(122833491,'B total123448405 less treasury614914'),('SSABa.ST','2024-06-30'):(295966330,'A shares after March buybacks/May cancellation'),('SSABb.ST','2024-06-30'):(700651337,'B shares after March buybacks/May cancellation')}
DENOM_URL={'BETSb.ST':'https://www.betssonab.com/sites/default/files/pr/202504032329-1.pdf?ts=1743753776','SSABa.ST':'https://www.ssab.com/en/news/2024/03/ssabs-share-buyback-program-is-now-completed-and-closed','SSABb.ST':'https://www.ssab.com/en/news/2024/03/ssabs-share-buyback-program-is-now-completed-and-closed'}
pd.DataFrame([dict(RIC=r,date=d,shares=s,note=n,source=DENOM_URL[r],raw_shares=SN.loc[(r,pd.Timestamp(d)),'shares']) for (r,d),(s,n) in DENOMS.items()]).to_csv(OUT/'denominator_overrides.csv',index=False)
json.dump({r:sorted(s) for r,s in ISINS.items()},open(OUT/'validated_isin_aliases.json','w'),indent=2)

def shares(ric,date):
 key=(ric,str(date.date()))
 return DENOMS[key][0] if key in DENOMS else SN.loc[(ric,date),'shares']

def security_check(e,window):
 c=CA.loc[(e.event_id,window)];b,a=c.before,c.after;r=e.RIC
 sb,sa=SN.loc[(r,b)],SN.loc[(r,a)];act=ACTIONS[(ACTIONS.RIC==r)&ACTIONS.action_date.gt(b)&ACTIONS.action_date.le(a)]
 f=float(act.factor.prod()) if len(act) else 1.;reasons=[];raw=c.raw_price_factor
 if r in UNRESOLVED_CLASS:reasons.append('unresolved_FI_share_class_labels')
 if not np.isfinite(raw):reasons.append('no_independent_price_unit_crosscheck')
 elif not len(act) and abs(raw-1)>.03:reasons.append('unresolved_nonunit_CA_diagnostic')
 elif len(act) and any(act.kind.eq('ordinary_split')) and abs(raw/f-1)>.03:reasons.append('split_factor_price_check_disagrees')
 s=shares(r,a);s0=shares(r,b)
 if not np.isfinite(s) or s<=0:reasons.append('missing_class_denominator')
 if pd.notna(sa.shares_date) and (a-sa.shares_date).days>7:reasons.append('stale_denominator_date')
 # Missing listings/IPO prices are never extrapolated backwards.
 if pd.isna(sb.close_date) or (b-sb.close_date).days>7:reasons.append('missing_or_stale_before_security')
 if pd.isna(sa.close_date) or (a-sa.close_date).days>7:reasons.append('missing_or_stale_after_security')
 # Large share-capital changes are not ordinary splits by assumption. Retain only if independently explained.
 capital=s/(s0*f) if np.isfinite(s0) and s0>0 else np.nan
 primary_issue=any(act.kind.str.contains('rights_issue'))
 if np.isfinite(capital) and not .85<=capital<=1.15 and not primary_issue:reasons.append('large_unexplained_share_capital_change')
 return dict(before=b,after=a,factor=f,denominator=s,before_denominator=s0,capital_ratio=capital,raw_price_factor=raw,ca_source=' | '.join(act.source),ca_kind=' | '.join(act.kind) if len(act) else 'screened_no_unit_change_not_exhaustive_CA_proof',security_exclusion=';'.join(reasons),primary_issue=primary_issue,denominator_override=(r,str(a.date())) in DENOMS)

# Explicit class suffixes are required when a share class exists in the event/RIC.
CLASS={}
for r,g in EVENTS.groupby('RIC'):
 z=re.search(r'([ab])\.ST',r)
 CLASS[r]=z.group(1).upper() if z else ('B' if g.company.str.contains(r'\bser\. B',regex=True).any() or r=='BICO.ST' else '')
MANUAL_BASE={'LAGRb.ST':{'LAGERCRANTZ','LAGERCRANTZ GROUP'},'HEBAb.ST':{'HEBA','HEBA FASTIGHETS'},'LATOb.ST':{'LATOUR','LATOUR INVESTMENTAB'},'DIOS.ST':{'DIOS'},'HNSA.ST':{'HANSA BIOPHARMA','HANSA MEDICAL'},'BICO.ST':{'BICO GROUP','CELLINK'},'MYCR.ST':{'MYCRONIC','MICRONIC'},'NP3.ST':{'NP3 FASTIGHETER','NP3 FASTIGHETER STAM'},'ONCO.ST':{'ONCOPEPTIDES','ONCOPETIDES'},'LUNDb.ST':{'LUNDBERGS','L E LUNDBERGFORETAGEN','LUNDBERGFORETAGEN'}}
BASES={r:{re.sub(r'\b[A-C]$','',norm(n)).strip() for n in g.company}|MANUAL_BASE.get(r,set()) for r,g in EVENTS.groupby('RIC')}
# Parenthesis can contain class in FI; AP class names here usually explicit final letter.
def baseclass(name):
 n=norm(name);n=re.sub(r'\b([ABC]) \1$',r'\1',n)
 z=re.search(r'\b([ABC])$',n);return (n[:z.start()].strip(),z.group(1)) if z else (n,'')
AP['_base']=AP.bolagsnamn.map(lambda x:baseclass(x)[0]);AP['_class']=AP.bolagsnamn.map(lambda x:baseclass(x)[1])
AP['_combined']=AP.samlat_aktieslag.astype(str).str.lower().eq('true')
# Same ordinary ISIN provides issuer-name aliases across dates without selecting on holdings changes.
isin_to_ric={i:r for r,ss in ISINS.items() for i in ss}
name_targets=AP.assign(_mapped=AP.ISIN.map(isin_to_ric)).dropna(subset=['_mapped']).groupby('_base')._mapped.agg(set)
for ric in BASES:
 BASES[ric]|={name for name,targets in name_targets.items() if targets=={ric}}
# A fuzzy candidate is never silently converted into absence. These reviewed pairs are
# different named issuers, or explicitly a different share class/instrument.
IGNORE_PREFIX={
 'ANODb.ST':['ASMODEE'], 'BHGF.ST':['NGS','BTS'], 'BICO.ST':['KAMBI','ACTIC','BALCO'],
 'CATE.ST':['CATELLA'], 'CINT.ST^H26':['4C','ACTIC','ITAB'], 'ETRN.ST^A22':['TRIANON'],
 'HNSA.ST':['SEDANA','XBRANE'], 'KARNO.ST':['PAGERO'], 'LIAB.ST':['BIOVICA','OEM','READLY','NILAR'],
 'NCAB.ST':['AQ GROUP','KAMBI','CARY','4C','ITAB'], 'NEWAb.ST':['AVEGA'], 'NOBI.ST':['NOBINA'],
 'NP3.ST':['NIVIKA','ALTRA','NEOBO'], 'SAVE.ST':['NORDEA'], 'SWECb.ST':['SWEDOL'],
 'THULE.ST':['HUMBLE'], 'TROAX.ST':['NORDAX','ITAB'], 'VBGb.ST':['AVEGA','BTS'],
 'VOLCARb.ST':['VOLVO AB-A','VOLVO AB-A SHS/B SHS']}

# Raw source checks contain all list totals, not the filtered Swedish-ISIN population.
SNAPSHOTS={(f,d):g for (f,d),g in AP.groupby(['fond','datum'])}
SOURCE={(f,d):g for (f,d),g in CHECK[CHECK.status.eq('parsed')].groupby(['fond','datum'])}
AP_LEDGER=[];AP_CACHE={}

def ap_snapshot(fund,ric,date):
 key=(fund,ric,date)
 if key in AP_CACHE:return AP_CACHE[key]
 out=dict(fund=fund,RIC=ric,date=date,quantity=np.nan,logical_zero=False,status='',source_file='',source_url='',source_rows='',source_names='',source_ISINs='',source_method='',price_ratio=np.nan)
 if (fund,date) not in SOURCE:out['status']='missing_complete_source_list'
 else:
  g=SNAPSHOTS.get((fund,date),pd.DataFrame());src=SOURCE[(fund,date)];out['source_file']=' | '.join(src.kallfil.astype(str))
  if not len(g):out['status']='empty_parsed_source_list'
  else:
   allowed=ISINS[ric]
   exact=g.ISIN.isin(allowed)&g.ISIN.ne('')
   candidate=g.RIC_kandidater.map(lambda x:ric in x.split('|'))
   clear_different=g.bolagsnamn.map(lambda x:any(norm(x).startswith(norm(v)) for v in IGNORE_PREFIX.get(ric,[])))
   clear_instrument=g.bolagsnamn.str.contains(r'\b(?:PREF|RTS|RIGHTS?|WARRANTS?|BTA|BTR|RDS)\b',case=False,regex=True)
   name_match=g._base.isin(BASES[ric])
   related=name_match|g.RIC.eq(ric)|(candidate&~clear_different&~clear_instrument)
   conflicting_isin=g.ISIN.ne('')&~g.ISIN.isin(allowed)
   # Only an explicitly different class/instrument clears an unmatched identifier.
   other_class_isins={'NCCb.ST':{'SE0000118952'},'INDUa.ST':{'SE0000107203'},'VOLVa.ST':{'SE0000115446'},'BONAVb.ST':{'SE0008091573'},'SSABa.ST':{'SE0000120669'},'SSABb.ST':{'SE0000171100'}}
   knownother=(g._class.ne('') & g._class.ne(CLASS[ric]))|clear_instrument|g.ISIN.isin(other_class_isins.get(ric,set()))
   knownother=knownother & ~g._combined
   unknown_related_isin=related&conflicting_isin&~knownother

   # Other-class ISINs/rights are not candidates for the target class. Combined rows remain ambiguous.
   explicit=name_match & g._class.eq(CLASS[ric]) & (bool(CLASS[ric])) & ~conflicting_isin
   single=name_match & g._class.eq('') & (not bool(CLASS[ric])) & ~conflicting_isin
   accept=(exact|explicit|single)&~g._combined&~g.excluded.isin(['non_share_instrument','private_credit_fund_or_debenture_not_listed_share','aggregate_parent_with_share_class_children'])
   unresolved=related&~accept&~knownother&~g.excluded.isin(['non_share_instrument','private_credit_fund_or_debenture_not_listed_share','aggregate_parent_with_share_class_children'])&(~g._class.ne('')|g._class.eq(CLASS[ric])|g._combined)
   if unresolved.any() or unknown_related_isin.any():out['status']='ambiguous_name_or_combined_share_classes'
   elif accept.any():
    z=g[accept];q=pd.to_numeric(z.antal_aktier,errors='coerce');mv=pd.to_numeric(z.marknadsvarde,errors='coerce')
    out.update(quantity=float(q.sum()),status='observed',source_url=' | '.join(z.kallurl.astype(str).unique()),source_rows=' | '.join(z.apply(lambda x:f'{x.kallfil}:p{x.kallsida}:r{x.kallrad}',axis=1)),source_names=' | '.join(z.bolagsnamn),source_ISINs=';'.join(sorted(set(z.ISIN)-{''})),source_method='exact_ordinary_ISIN_or_explicit_class_normalized_name')
    if q.isna().any() or q.lt(0).any():out.update(quantity=np.nan,status='invalid_AP_quantity')
    pr=SN.loc[(ric,date),'fi_price']
    if q.sum()>0 and mv.sum()>1000000 and np.isfinite(pr) and pr>0:
     ratio=mv.sum()/q.sum()/pr;out['price_ratio']=ratio
     # Five percent includes MSEK rounding; very small positions are not validated by this diagnostic.
     if abs(ratio-1)>.05:out.update(quantity=np.nan,status='AP_quantity_value_unit_check_failed')
   else:
    # Complete published list + explicit identity dictionary + no unresolved related row.
    out.update(quantity=0.,logical_zero=True,status='absent_from_complete_parsed_list',source_url=' | '.join(g.kallurl.astype(str).unique()),source_method='complete_list_absence_identity_checked')
 AP_CACHE[key]=out;AP_LEDGER.append(out);return out

# FI valid nonempty report presence is required at both dates. Quantity=0 only within such reports.
FUND_DATES={d:set(g.Fond_institutnummer.astype(int)) for d,g in META.groupby('Kvartalsslut')}
FOND_META=META.drop_duplicates(['Fond_institutnummer','Kvartalsslut']).set_index(['Fond_institutnummer','Kvartalsslut'])
FI_CACHE={};FI_LEDGER=[];BAD_KEYS={r:set(map(tuple,g[['Kvartalsslut','Fond_institutnummer']].drop_duplicates().to_numpy())) for r in EVENTS.RIC.unique() for g in [BADH[BADH['ISIN-kod_instrument'].isin(ISINS[r])]]}
# Prepare security-date-fund totals once, not repeatedly per event.
for ric in EVENTS.RIC.unique():
 z=H[H['ISIN-kod_instrument'].isin(ISINS[ric])].copy()
 z['bad_unit']=False
 for date,zz in z.groupby('Kvartalsslut'):
  pr=SN.loc[(ric,date),'fi_price'];rr=zz.Marknadsvärde_instrument/zz.Antal/pr
  invalid=zz.Valuta.eq('SEK')&zz.Antal.gt(0)&zz.Marknadsvärde_instrument.gt(10000)&((rr-1).abs()>.10)
  z.loc[zz.index,'bad_unit']=invalid
 sums=z.groupby(['Kvartalsslut','Fond_institutnummer']).agg(quantity=('Antal','sum'),bad_unit=('bad_unit','any'),ISINs=('ISIN-kod_instrument',lambda a:';'.join(sorted(set(a)))),names=('Instrumentnamn',lambda a:' | '.join(sorted(set(a.dropna())))))
 FI_CACHE[ric]=sums

MANDATES=[dict(group='documented_Nordnet_OMXSB_family',fund_id=60320,from_date='2018-12-31',to_date='2025-12-31',definition='OMXSBGI until2022-05-31; OMXSBESGGI from2022-06-01; same ID and fundISIN across2022-10-01 manager transfer',evidence='Nordnet2022annualp4; ENF2019p1; FIquartermetadata',source='https://nordnetab.com/wp-content/uploads/2023/05/Arsberattelse-Nordnet-Indexfond-Sverige-ESG-2022.pdf'),dict(group='metadata_supported_Nordea_OMXSBCAP',fund_id=60293,from_date='2018-12-31',to_date='2025-12-31',definition='FI reports Sverige Passiv, OMX Stockholm Benchmark Cap100%; historical prospectus not independently obtained',evidence='FIoriginalquarterreports; not identical evidentiary status as dated Nordnet documentation',source='data/derived/fi/fi_holdings_long.csv.gz')]
pd.DataFrame(MANDATES).to_csv(OUT/'tracker_definition_sources.csv',index=False)

OBS=[];VALID=[]
for e in EVENTS.itertuples():
 for window in ['event','prior']:
  c=security_check(e,window);b,a=c['before'],c['after'];rec=dict(event_id=e.event_id,RIC=e.RIC,company=e.company,type=e.type,review_cycle=e.review_cycle,window=window,**c)
  groups={};reasons=[]
  for fund in ['AP2','AP3','AP4']:
   qb=ap_snapshot(fund,e.RIC,b);qa=ap_snapshot(fund,e.RIC,a)
   rec[fund+'_before']=qb['quantity'];rec[fund+'_after']=qa['quantity'];rec[fund+'_before_zero']=qb['logical_zero'];rec[fund+'_after_zero']=qa['logical_zero'];rec[fund+'_status_before']=qb['status'];rec[fund+'_status_after']=qa['status']
   groups[fund]=(qb['quantity'],qa['quantity'])
   if fund in ['AP3','AP4'] and not np.isfinite(qb['quantity']+qa['quantity']):reasons.append(fund+':'+qb['status']+'|'+qa['status'])
  available=FUND_DATES.get(b,set())&FUND_DATES.get(a,set());sums=FI_CACHE[e.RIC];fi={};bad=[]
  for f in sorted(available):
   q=[];invalid=any((d,f) in BAD_KEYS.get(e.RIC,set()) for d in [b,a]);ambiguous_signed_quantity=invalid;details=[]
   for d in [b,a]:
    if (d,f) in sums.index:
     zz=sums.loc[(d,f)];q.append(zz.quantity);invalid|=bool(zz.bad_unit);details.append(zz.ISINs)
    else:q.append(0.);details.append('')
   fi[f]=q if not invalid else (np.nan,np.nan)
   if invalid:bad.append(f)
   if q[0] or q[1] or invalid or f in [60320,60293]:
    FI_LEDGER.append(dict(event_id=e.event_id,window=window,RIC=e.RIC,fund_id=f,before=b,after=a,quantity_before_raw=q[0],quantity_after_raw=q[1],unit_invalid=invalid,ambiguous_signed_or_missing_quantity=ambiguous_signed_quantity,ISIN_before=details[0],ISIN_after=details[1],is_documented_Nordnet=f==60320,is_metadata_Nordea=f==60293,is_original14=f in BEHAVIORAL))
  good={f:q for f,q in fi.items() if np.isfinite(sum(q))}
  rec['FI_matched_report_funds']=len(available);rec['FI_valid_unit_funds']=len(good);rec['FI_invalid_unit_funds']=';'.join(map(str,bad))
  def aggregate(ids):
   a0=[q for f,q in good.items() if f in ids];return tuple(np.sum(a0,axis=0)) if a0 else (np.nan,np.nan)
  groups['FI_all_matched']=aggregate(set(good));groups['FI_Nordnet_documented']=aggregate({60320});groups['FI_Nordea_metadata']=aggregate({60293});groups['FI_two_trackers']=aggregate({60320,60293});groups['FI_original14']=aggregate(BEHAVIORAL);groups['FI_other_than_Nordnet']=aggregate(set(good)-{60320});groups['FI_other_than_14']=aggregate(set(good)-BEHAVIORAL)
  rec['FI_original14_available']=len(BEHAVIORAL&set(good));rec['Nordnet_identity_link_verified']=60320 in available and all(str(FOND_META.loc[(60320,d),'Fond_ISIN-kod'])=='SE0002756973' for d in [b,a])
  if not rec['Nordnet_identity_link_verified']:reasons.append('Nordnet_report_or_identity_missing')
  if 60320 not in good:reasons.append('Nordnet_missing_or_unit_invalid')
  rec['Nordnet_strategy_change_halfyear']=b<pd.Timestamp('2022-06-01')<=a
  rec['Nordnet_manager_transfer_halfyear']=b<pd.Timestamp('2022-10-01')<=a
  # AP2 is separately labelled net of lending; never in APsum.
  groups['AP3_AP4_sum']=tuple(np.array(groups['AP3'])+np.array(groups['AP4']))
  for name,(qb,qa) in groups.items():
   rec[name+'_before_raw']=qb;rec[name+'_after_raw']=qa
   rec[name+'_before_adjusted']=qb*c['factor']
   rec[name+'_delta_pp']=100*(qa-qb*c['factor'])/c['denominator'] if c['denominator']>0 else np.nan
  if c['security_exclusion']:reasons.append(c['security_exclusion'])
  rec['exclusion']=';'.join(reasons);rec['valid']=not reasons
  rec['other_OMXSB_event_in_interval']=bool(((EVENTS.RIC==e.RIC)&EVENTS.ED.gt(b)&EVENTS.ED.le(a)&EVENTS.event_id.ne(e.event_id)).any())
  # Check the original full event census, not merely the quantity-available frozen sample.
  OBS.append(rec)

OBS=pd.DataFrame(OBS)
FULL=pd.read_csv(ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',parse_dates=['effective_date'])
for i,r in OBS.iterrows():
 OBS.loc[i,'other_OMXSB_event_in_interval']=bool(((FULL.RIC==r.RIC)&FULL.effective_date.gt(r.before)&FULL.effective_date.le(r.after)&FULL.event_id.ne(r.event_id)).any())
OBS['days']=(OBS.after-OBS.before).dt.days
OBS['direction']=np.where(OBS.type.eq('addition'),1,-1)
OBS['main_common_sample']=OBS.valid & OBS.window.eq('event')
valid_prior=set(OBS.loc[OBS.valid&OBS.window.eq('prior')&~OBS.other_OMXSB_event_in_interval,'event_id'])
valid_event=set(OBS.loc[OBS.main_common_sample,'event_id']);paired=valid_event&valid_prior
OBS['paired_background_sample']=OBS.event_id.isin(paired)
# For the background comparison FI also needs the SAME funds at all three endpoints.
# Keep these columns separate: main event estimates must not select on prior availability.
PAIR_FUNDS=[]
for eid in sorted(paired):
 e=EVENTS[EVENTS.event_id.eq(eid)].iloc[0];dates=[e.prior,e.before,e.after];sums=FI_CACHE[e.RIC]
 ff=set.intersection(*(FUND_DATES.get(d,set()) for d in dates));good3={}
 for f in sorted(ff):
  vals=[];invalid=False
  for d in dates:
   invalid|=(d,f) in BAD_KEYS.get(e.RIC,set())
   if (d,f) in sums.index:
    zz=sums.loc[(d,f)];vals.append(zz.quantity);invalid|=bool(zz.bad_unit)
   else:vals.append(0.)
  if not invalid:good3[f]=vals
  if any(vals) or invalid:PAIR_FUNDS.append(dict(event_id=eid,RIC=e.RIC,fund_id=f,quantity_prior=vals[0],quantity_before=vals[1],quantity_after=vals[2],excluded_invalid_quantity=invalid))
 sets={'FI_all_matched':set(good3),'FI_Nordnet_documented':{60320},'FI_Nordea_metadata':{60293},'FI_two_trackers':{60320,60293},'FI_original14':BEHAVIORAL,'FI_other_than_Nordnet':set(good3)-{60320},'FI_other_than_14':set(good3)-BEHAVIORAL}
 for win,ib,ia in [('event',1,2),('prior',0,1)]:
  idx=OBS.index[OBS.event_id.eq(eid)&OBS.window.eq(win)][0]
  OBS.loc[idx,'FI_balanced_three_date_funds']=len(good3)
  for group,ids in sets.items():
   q=[v for f,v in good3.items() if f in ids]
   arr=np.sum(q,axis=0) if q else [np.nan]*3
   OBS.loc[idx,group+'_balanced3_delta_pp']=100*(arr[ia]-OBS.loc[idx,'factor']*arr[ib])/OBS.loc[idx,'denominator']
pd.DataFrame(PAIR_FUNDS).to_csv(OUT/'fi_balanced_background_fund_observations.csv.gz',index=False,compression='gzip')
OBS.to_csv(OUT/'ownership_observations.csv',index=False)
pd.DataFrame(AP_LEDGER).to_csv(OUT/'ap_snapshot_resolution.csv',index=False)
pd.DataFrame(FI_LEDGER).to_csv(OUT/'fi_fund_event_observations.csv.gz',index=False,compression='gzip')
# Disjoint group and sum identities are checks of accounting, not behavioral evidence.
for g in ['before_raw','after_raw','delta_pp']:
 ok=OBS[['AP3_'+g,'AP4_'+g,'AP3_AP4_sum_'+g]].dropna()
 assert np.allclose(ok['AP3_'+g]+ok['AP4_'+g],ok['AP3_AP4_sum_'+g])
 ok=OBS[['FI_Nordnet_documented_'+g,'FI_other_than_Nordnet_'+g,'FI_all_matched_'+g]].dropna()
 assert np.allclose(ok.iloc[:,0]+ok.iloc[:,1],ok.iloc[:,2])
assert OBS.event_id.nunique()==230 and OBS.review_cycle.nunique()==14
assert OBS[['event_id','window']].duplicated().sum()==0

# Review-clustered inference for the event-weighted mean, with CR1 and t(G-1).
def stats(df,col):
 z=df[['review_cycle',col]].dropna();n=len(z);G=z.review_cycle.nunique();mean=z[col].mean()
 if G>1 and n>1:
  score=(z[col]-mean).groupby(z.review_cycle).sum();se=math.sqrt(G/(G-1)*float((score**2).sum())/(n*n));q=t.ppf(.975,G-1)
  lo,hi=mean-q*se,mean+q*se
 else:se=lo=hi=np.nan
 rv=z.groupby('review_cycle')[col].mean();rse=rv.std(ddof=1)/math.sqrt(G) if G>1 else np.nan
 return dict(N=n,G=G,mean_pp=mean,se_review_cluster=se,ci95_low=lo,ci95_high=hi,median_pp=z[col].median(),equal_review_mean_pp=rv.mean(),equal_review_ci95_low=rv.mean()-t.ppf(.975,G-1)*rse if G>1 else np.nan,equal_review_ci95_high=rv.mean()+t.ppf(.975,G-1)*rse if G>1 else np.nan)
GROUPS=['AP3','AP4','AP3_AP4_sum','FI_Nordnet_documented','FI_Nordea_metadata','FI_two_trackers','FI_original14','FI_other_than_Nordnet','FI_other_than_14','FI_all_matched','AP2']
RESULTS=[]
def balanced_background(z):
 z=z.copy()
 for group in GROUPS:
  if group.startswith('FI_'):z[group+'_delta_pp']=z[group+'_balanced3_delta_pp']
 return z
SETS={'main_common':OBS[OBS.main_common_sample],'no_large_capital_change':OBS[OBS.main_common_sample&OBS.capital_ratio.between(.95,1.05)&~OBS.primary_issue],'fixed_Nordnet_strategy':OBS[OBS.main_common_sample&~OBS.Nordnet_strategy_change_halfyear],'paired_event':balanced_background(OBS[OBS.paired_background_sample&OBS.window.eq('event')]),'paired_prior':balanced_background(OBS[OBS.paired_background_sample&OBS.window.eq('prior')])}
for sample,df in SETS.items():
 for direction in ['addition','deletion','direction_aligned_pooled']:
  sub=df.copy() if direction=='direction_aligned_pooled' else df[df.type.eq(direction)].copy()
  for group in GROUPS:
   col=group+'_delta_pp';sub['value']=sub[col]*(sub.direction if direction=='direction_aligned_pooled' else 1)
   RESULTS.append(dict(sample=sample,direction=direction,group=group,**stats(sub,'value')))
# Paired period-normalized difference, fixed same events, cannot identify a causal response.
E=balanced_background(OBS[OBS.paired_background_sample&OBS.window.eq('event')]).set_index('event_id');B=balanced_background(OBS[OBS.paired_background_sample&OBS.window.eq('prior')]).set_index('event_id')
for direction in ['addition','deletion','direction_aligned_pooled']:
 sub=E.copy() if direction=='direction_aligned_pooled' else E[E.type.eq(direction)].copy()
 for group in GROUPS:
  col=group+'_delta_pp';sub['value']=182.625*(sub[col]/sub.days-B.loc[sub.index,col]/B.loc[sub.index,'days'])*(sub.direction if direction=='direction_aligned_pooled' else 1)
  RESULTS.append(dict(sample='paired_event_minus_prior_182625day',direction=direction,group=group,**stats(sub,'value')))
RES=pd.DataFrame(RESULTS);RES.to_csv(OUT/'ownership_results.csv',index=False)
# Full sample/exclusion journal and source reconciliation.
OBS.loc[~OBS.valid,['event_id','RIC','window','before','after','exclusion']].to_csv(OUT/'exclusion_journal.csv',index=False)
why=OBS.loc[~OBS.valid,['window','event_id','exclusion']].assign(reason=lambda x:x.exclusion.str.split(';')).explode('reason');why.groupby(['window','reason']).event_id.nunique().rename('events').reset_index().to_csv(OUT/'exclusion_counts.csv',index=False)
coverage=OBS.groupby(['window','review_cycle','type']).agg(candidates=('event_id','size'),valid=('valid','sum'),common_main=('main_common_sample','sum'),paired=('paired_background_sample','sum')).reset_index();coverage.to_csv(OUT/'sample_coverage.csv',index=False)
recon=[]
for f,d,annual in [('AP3','2019-12-31',51401e6),('AP4','2019-12-31',78046e6),('AP3','2024-12-31',69444e6),('AP4','2024-12-31',99249e6)]:
 z=CHECK[(CHECK.fond==f)&CHECK.datum.eq(d)]
 recon.append(dict(fund=f,date=d,annual_swedish_equity_SEK=annual,full_list_extracted_SEK=z.extracted_total_sek.iloc[0],difference_SEK=z.extracted_total_sek.iloc[0]-annual,scope='full_published_Swedish_portfolio_including_nonSE_ISIN_and_private_positions; filtered_analysis_list_not_comparable',loans='annual_accounting_note_keeps_lent_securities_on_balance_sheet',source='data/raw/omxsb_extension_20261031/support/gov_ap_'+d[:4]+'.pdf'))
pd.DataFrame(recon).to_csv(OUT/'AP_reporting_reconciliation.csv',index=False)
SUMMARY=dict(main_candidates=230,main_common=int(OBS.main_common_sample.sum()),main_reviews=int(OBS[OBS.main_common_sample].review_cycle.nunique()),paired_events=len(paired),paired_reviews=int(E.review_cycle.nunique()),AP_snapshot_logical_zeros=int(pd.DataFrame(AP_LEDGER).logical_zero.sum()),main_AP_endpoint_zero_counts={f:int(OBS.loc[OBS.main_common_sample,[f+'_before_zero',f+'_after_zero']].sum().sum()) for f in ['AP3','AP4']},main_N_by_direction=OBS[OBS.main_common_sample].type.value_counts().to_dict(),accounting_checks='passed',interpretation='quarter/halfyear holdings changes, not executed trades or transaction counterparties; no return regressions')
(OUT/'run_summary.json').write_text(json.dumps(SUMMARY,indent=2));print(json.dumps(SUMMARY,indent=2));print(RES[(RES['sample']=='main_common')&RES.group.isin(['AP3','AP4','AP3_AP4_sum','FI_Nordnet_documented','FI_original14','AP2'])].to_string(index=False))

# Descriptive ownership levels on the same common sample. The normalized before
# level uses after-S; only that level subtracts exactly to the primary net-change.
LEVELS=[]
main=OBS[OBS.main_common_sample].copy()
for direction in ['addition','deletion']:
 z=main[main.type.eq(direction)].copy()
 for group in GROUPS:
  for measure,values in [('before_ownership_pct',100*z[group+'_before_raw']/z.before_denominator),('before_adjusted_per_after_S_pct',100*z[group+'_before_adjusted']/z.denominator),('after_ownership_pct',100*z[group+'_after_raw']/z.denominator)]:
   z['value']=values;LEVELS.append(dict(direction=direction,group=group,measure=measure,**stats(z,'value')))
pd.DataFrame(LEVELS).to_csv(OUT/'ownership_levels.csv',index=False)
# Quantify the data-cleaning contribution; this is not a signed-net economic series.
ff=pd.DataFrame(FI_LEDGER);invalid=ff[ff.unit_invalid&ff.window.eq('event')].merge(main[['event_id','factor','denominator','type','direction']],on='event_id')
invalid['excluded_positive_only_delta_pp']=100*(invalid.quantity_after_raw-invalid.factor*invalid.quantity_before_raw)/invalid.denominator
invalid.to_csv(OUT/'excluded_FI_positive_only_contributions.csv',index=False)
impact=[]
for direction in ['addition','deletion','direction_aligned_pooled']:
 z=main if direction=='direction_aligned_pooled' else main[main.type.eq(direction)]
 bad=invalid if direction=='direction_aligned_pooled' else invalid[invalid.type.eq(direction)]
 contribution=(bad.excluded_positive_only_delta_pp*(bad.direction if direction=='direction_aligned_pooled' else 1)).sum()/len(z)
 impact.append(dict(direction=direction,N_events=len(z),excluded_fund_event_pairs=len(bad),change_in_mean_from_dropping_positive_only_pairs_pp=-contribution,scope='not signed-netting; ambiguous whole fund-security pair removed at both endpoints'))
pd.DataFrame(impact).to_csv(OUT/'FI_quantity_exclusion_impact.csv',index=False)

import platform, scipy
versions=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,scipy=scipy.__version__)
(OUT/'runtime_versions.json').write_text(json.dumps(versions,indent=2))
LABELS={'AP3':'AP3','AP4':'AP4','AP3_AP4_sum':'AP3 + AP4','FI_Nordnet_documented':'Nordnet, daterat dokumenterad','FI_Nordea_metadata':'Nordea, historiska FI-metadata','FI_original14':'Original14, beteendevalda','FI_other_than_14':'Övriga observerade FI (blandad grupp)','AP2':'AP2, netto efter utlåning'}
selected=RES[RES['sample'].eq('main_common')&RES.group.isin(LABELS)&~RES.direction.eq('direction_aligned_pooled')].copy();selected['grupp_sv']=selected.group.map(LABELS);selected.to_csv(OUT/'RESULTAT_OVERSIKT.csv',index=False)
rows=[]
for group in LABELS:
 vals=[]
 for direction in ['addition','deletion']:
  a=selected[selected.group.eq(group)&selected.direction.eq(direction)].iloc[0]
  vals.append(f'{a.mean_pp:+.3f} [{a.ci95_low:+.3f}; {a.ci95_high:+.3f}]')
 rows.append(f'{LABELS[group]}: tillägg {vals[0]}; borttag {vals[1]}')
(OUT/'ANALYSRAPPORT.txt').write_text('''OMXSB: genomförd ägaranalys 2019–2025
Gransknings- och analysunderlag, 2026-10-31. Inte uppsatstext.

RESULTAT OCH TOLKNING
AP3 och AP4 kan inte på detta underlag beskrivas som en stabil nettomotvikt till indexrelaterade innehavsförändringar. AP-summans huvudmedel pekar svagt åt motsatt håll, men intervallen innefattar både med- och motriktade förändringar. AP3:s riktningsjusterade medel är praktiskt nära noll. Den förutbestämda bakgrundsjämförelsen ändrar AP-summans punkttecken. Detta visar osäkerhet, inte att AP aldrig säljer eller köper, och inte att Greenwood–Sammons amerikanska motpartsmekanism saknas i Sverige.

Gemensamt urval: 217 av 230 låsta event, 119 tillägg och 98 borttag, samtliga 14 reviews. Alla huvudgrupper jämförs på samma event. Resultaten är procentenheter av det berörda aktieslagets utestående aktier vid halvårets slut. Exempel: 0,10 pp motsvarar en nettoökning med 0,10 procent av aktieslaget. Intervallet är 95 procent, CR1 på review med t(13).

'''+'\n'.join(rows)+'''

För både riktningar tillsammans vänds tecknet för borttag. AP3+AP4 blir då −0,066 pp, 95%CI [−0,272; +0,140]. Ett negativt värde är motriktat indexändringen, inte bevis för att fonden sålde direkt till en tracker. Nordnets motsvarande medel är +0,070 pp [0,055; 0,085]. Original 14:s +0,993 pp är en replikationskänslighet: gruppen valdes tidigare delvis utifrån sitt handelsbeteende och är ingen oberoende mandatdefinition.

BAKGRUND OCH FÖRUTBESTÄMDA KÄNSLIGHETER
133 event (79 tillägg, 54 borttag) över 13 reviews har både ett giltigt eventhalvår och ett giltigt närmast föregående halvår utan annan ordinarie OMXSB-händelse i aktien. Samma event används i båda perioder. FI jämför dessutom exakt samma fond-ID vid alla tre rapportdatum och tar bort hela fond–värdepapper-paret om någon av de tre kvantiteterna är oklar. Antal dagar normaliseras till182,625 dagar.
AP-summans riktningsjusterade event-minus-prior är +0,141 pp [−0,126; +0,409]. Enbart eventhalvåret på detta delurval är −0,064 pp; föregående halvår är −0,206 pp. Dessa är deskriptiva jämförelser, inte en kausal DiD: förperioden väljer inte en motsvarande obehandlad aktie och indexurval kan följa tidigare företagsutveckling.
Med en snävare kapitalförändringsgräns (±5%, inga kända nyemissioner) återstår 207 event och AP-summan är −0,049 pp [−0,234; +0,135]. Utan halvåret då Nordnet bytte till ESG-index återstår 195 event/13 reviews och AP-summan är −0,022 pp [−0,232; +0,187]. Lika vikt per review ger −0,013 pp i huvudurvalet. Inget av dessa planerade mått ger en stabil tydlig AP-motvikt.

VAD SOM FAKTISKT MÄTS
Utfallet är 100*(antal_efter − splitfaktor*antal_före)/utestående_aktier_efter. Råa FI-Antal används; tidigare exporters redan splitjusterade idx_b återanvänds inte. Innehavsförändringen kan komma från marknadstransaktioner, fondflöden, nyemissioner, konverteringar och vanlig omviktning. Exempelvis CTEK:s emission ändrar innehav utan att visa en transaktionsmotpart. Normaliserat föreägande och faktiskt föreägande med dåtidens nämnare hålls isär i ownership_levels.csv. Rättighets- och inlöseninstrument med egna ISIN läggs inte till ordinarie aktier.
AP3/AP4 redovisas var för sig och summeras exakt, utan residualgrupp. AP2 har rapporterat netto efter utlånade aktier och är därför separat; förändrade utlån kan påverka dess serie. År2026 ingår inte i denna analys på grund av AP1-överföringar och ofullständigt jämförbart år.

MANDAT OCH FI-POPULATION
Nordnet 60320 är huvudgruppens dokumenterade tracker. Daterad 2019-källa anger OMXSBGI; årsrapport 2022 anger OMXSBGI fram till 2022-06-01, därefter OMXSBESGGI. FI-ID och fond-ISIN SE0002756973 är oförändrade vid förvaltarbytet 2022-10-01. Detta verifierar fondkontinuitet, inte att varje OMXSB-event är en obligatorisk transaktion i ESG-indexet.
Nordea 60293 visas separat: historiska FI-rapporter säger Sverige Passiv och OMX Stockholm Benchmark Cap 100%, men ett samtida tidigt prospekt har inte hämtats. Gruppen med två trackers är en transparens-/täckningskänslighet. Den dokumenterade delgruppen är ofullständig och mäter inte hela svensk passiv nettoefterfrågan.
Alla FI betyder observerade rapporterande svenska FI-fonder med giltig rapport och kvantitet på båda datum. 535–654 fond-ID har matchade rapporter,534–654 efter kvantitetskontroll; många äger inte den aktuella aktien. Original 14 är närvarande vid båda datum i alla huvudceller. Övriga FI innehåller både aktiva, passiva och okända mandat och kallas aldrig automatiskt aktiva fonder.

IDENTITET, NOLLOR OCH REDOVISNING
Fulla publicerade svenska AP-portföljer används, inklusive utlandsdomicilierade värdepapper. Det filtrerade SE-ISIN-urvalet används inte för att bevisa frånvaro. Frånvaro är 0 endast när komplett parsad lista finns och ingen olöst relevant rad återstår. Exakta vanliga ISIN och explicita aktieslag prioriteras. Fuzzyförslag godkänner aldrig en matchning. Äldre Lundbergs-namn och stavningen Oncopetides har granskats; namn som samma källa använder för flera olika ISIN/bolag får inte okritiskt bli alias. Sammanslagna A/B-rader får inte fördelas godtyckligt eller skapa en falsk nolla. NCC A togs uttryckligen bort från NCC B:s aliasunion.
I huvudurvalet finns99 AP3- och208 AP4-ändpunkter med logisk frånvaronolla, inklusive både fulla inträden och utträden. Den separata PDF-kontrollen söker samtliga ordinarie alias-ISIN i originalen för alla 696 logiska nollor i alla fonder/fönster:48 originalfiler, inga ISIN-konflikter. Äldre listor utan ISIN kräver fortfarande den redovisade namn-/klasskontrollen; en negativ ISIN-sökning ensam bevisar inte frånvaro.
AP3/AP4 årsredovisningar 2019 och 2024 anger att utlånade aktier kvarstår i balansräkningen. Fulla listsummor stäms av mot svenska aktier i årsrapporten: AP3-avvikelser −0,217/−0,111 MSEK; AP4 −0,030/+1,000 MSEK, förenliga med avrundning. 2024 AP4:s filtrerade lista 98 257 MSEK får inte jämföras med hela redovisade innehavet 99 249 MSEK. Avstämningen stöder definitionen och extraktionen; den är inte en separat revisionsbekräftelse för varje halvår.

BOLAGSHÄNDELSER OCH KVARVARANDE DATAOSÄKERHET
Verifierade ordinarie splitfaktorer: Lagercrantz 3, Addnode 4, Heba 2, Fortnox 10; för bakgrundsfönster även Lifco 5, Hexatronic 5, BioGaia 5. Separata inlösenaktier ändrar inte i sig antalet kvarvarande ordinarie aktier. Betssons felaktigt dubblerade LSEG-nämnare korrigeras med primär årsrapport: 2023-12-31 utestående B 121 374 972 och 2024-12-31 utestående B 122 833 491. SSAB 2024-06-30korrigeras för genomförda återköp. Alla justeringar, källor och datumprecision finns i maskinläsbara journaler.
13 event utesluts:8 har oklar AP4-namn-/klassrad,5 har stor ännu inte verifierad förändring av aktiekapitalet och 1 har olösta Embracer A/B-etiketter; en observation har två skäl. Övriga bolagshändelser screenas med oberoende FI-priser, justerade LSEG-priser, aktieantal, datum och innehavens värde/antal. En prisratio nära 1 är inte ett bevis för att alla bolagshändelser saknas. Samtliga kvarvarande aktieslagsnämnare har inte manuellt stämts av mot varje emittents rapport; detta är en konkret kvarvarande kvalitetssäkringsgräns.
198 FI-rårader har negativt Antal, delvis VPL/utlåningsetiketter och ibland nollmarknadsvärde. De nettas inte blint och försvinner inte till en falsk nolla. Hela fond–värdepapper-paret tas bort vid båda endpoints om någon ändpunkt är oklar:59 fond–event–fönsterpar (28 eventfönster, 31 bakgrundsfönster) i den låsta populationen. Ingen Nordnet/Nordea-post påverkas. I bakgrunden med tre datum används motsvarande gemensamma giltiga fondpopulation. I det gemensamma huvudurvalet berörs 24 fond–event-par. Att ta bort dessa i stället för att felaktigt behålla enbart positiva kvantiteter ändrar övriga FI:s medel med −0,000055 pp för tillägg och +0,007791 pp för borttag. Detta är en redovisningskorrigering, ingen uppskattning av ekonomiskt nettade korta/långa positioner. Exakta observationer och bidrag finns exporterade.

VAD RESULTATET INTE KAN AVGÖRA
Halvårsdata visar varken handelsdatum runt annonsering/implementering eller köpare och säljare i samma transaktion. De identifierar inte marknadens totala absorption, utländska ägare, hushåll eller kausalt prisutbud. Matchade fondrapporter eliminerar inte alla fondflöden/vanliga omviktningar. 14 reviews är få; t-intervallen är småklusteranpassade men ger inte säkert skydd mot kvarvarande beroende över tiden eller samma återkommande företag. Det breda intervallet utesluter inte ekonomiskt relevanta motriktade förändringar. Ingen ny CAR-regression, efterfrågeelasticitet, FTN-avkastning eller uppsatstext har producerats.

LEVERANS
ownership_observations.csv innehåller samtliga 230 event i båda fönster, råa/justerade kvantiteter, nämnare, gruppsummor, klass-/CA-/nollflaggor och exklusionsorsaker. ap_snapshot_resolution.csv har exakt källfil/sida/rad för positiva innehav samt frånvarogrund. FI-ledger, balanserad bakgrundsledger, resultat, nivåer, täckning, exklusionsjournal, källor, hashlistor och kontrollresultat följer med. KORNING.txt beskriver reproduktion. Ingen commit/push och inga gamla baslinjer har skrivits över.
''')
(OUT/'KORNING.txt').write_text('''Reproduktion från reporoten

Python 3 med pandas, numpy, scipy, pyarrow samt pdftotext (Poppler) på PATH.
Den verifierade körningen använde /opt/anaconda3/bin/python3. Versioner: runtime_versions.json.

python3 code/build/omxsb_ap_prepare.py
python3 code/build/omxsb_ap_ownership.py
python3 code/build/omxsb_ap_validate.py

Alla tre accepterar --repo /absolut/repo och --out /absolut/utdata. Samma --out ska användas i alla tre. Default är output/omxsb_extension_20261031/ownership. Kör inte parallellt mot samma outputmapp. Inga nätanrop görs. Originaldata och äldre exporter läses men skrivs inte.

Väsentliga inputfiler: AP-innehav inklusive excluded_rows/source_checks/parse_rejections; FI fi_holdings_long.csv.gz; LSEG stocks_daily_2005.parquet (inte den skadade CSV-filen); OMXSB-eventfil; corrected/nettrading_omxsb.csv endast för låst population/ISIN-kandidater; corrected/index_funds.csv endast original14-känslighet; historical_isin_name_flags.csv för granskning. AP-PDF-original krävs för sista nollkontrollen. Exakt datahash och källfilhash finns i input_hashes.json och execution_source_hashes.json. Sökvägar i källjournaler är relativa till repot.

PROTOKOLL.txt låstes före nya AP-utfall. IMPLEMENTATION_CORRECTIONS.txt dokumenterar datalogikfel som hittades vid efterföljande kodgranskning och rättades utan utfallsstyrt urval. Korrektioner för bolagshändelser, nämnare och mandat är explicita i koden och exporterade källjournaler. En komplett års-/halvårscensus av varje emittents bolagshändelser har inte erhållits; se rapportens begränsningar.

Utdata kan återskapas deterministiskt med angivna indata. ownership_results.csv innehåller alla förutbestämda grupper/specifikationer, utan val efter p-värden. validate-körningen testar gruppbokföring, CR1-intervall, negativa FI-poster och frånvaro mot original-PDF:er. Standardkörningen ska avsluta med 0 konflikter och exitkod 0.
''')
