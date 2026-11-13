# Indexfonder efter innehav, 2 nov 2026. För varje kvartal och fond: hur lik är svenska aktiedelen en ren OMXSB-indexfond?
# Referens Swedbank Robur Access Sverige (60824, OMXSB Cap GI), annars Nordea Sverige Passiv (60293); kvoten antal_fond/antal_ref ska vara ungefär lika för alla aktier hos en OMXSB-följare.
# Regel (ny definition av OMXSB-indexfond per kvartal):
#   A) följer enligt innehavet: täckning >= 0,8, andel aktier utanför referensen < 0,25, robust spridning (MAD) i log-kvot < 0,45; eller
#   B) OMXSB i jämförelseindex och indexlik (bred eller indexnamn) och innehavet inte motsäger det: täckning >= 0,6, spridning <= 0,7, utanför <= 0,25.
import sys, numpy as np, pandas as pd
# Körs från code/claude_checks: python3 agar_kontroll/indexfond_innehav.py (kräver data/fi_all_holdings.pkl, byggs av fi_parse_all.py)
H = pd.read_pickle('data/fi_all_holdings.pkl')
H['antal'] = pd.to_numeric(H.antal.astype(str).str.replace(',', '.').str.replace(' ', ''), errors='coerce')
H = H[(H.antal > 0) & H['isin'].astype(str).str.startswith('SE')].copy(); H['fund_id'] = H.fund_id.astype(str)
F = pd.read_csv('data/fi_all_funds_klass.csv'); F['fund_id'] = F.fund_id.astype(str); F = F.drop_duplicates(['q', 'fund_id'], keep='last')
j = F.jmf.fillna('').str.lower(); F['B'] = j.str.contains(r'stockholm benchmark|omxsb|\bsbx')
F['namnindex'] = F.namn.astype(str).str.contains('index|indexnära|exponering|etf|xact|passiv|access', case=False)
rows = []
for q, h in H.groupby('q'):
    A = h.groupby(['fund_id', 'isin']).antal.sum()
    refid = '60824' if '60824' in A.index.get_level_values(0) else '60293'
    ref = A.loc[refid]
    for f, a in A.groupby(level=0):
        a = a.droplevel(0); com = a.index.intersection(ref.index)
        if len(com) < 10: continue
        lr = np.log(a[com] / ref[com])
        rows.append(dict(q=q, fund_id=f, ref=refid, tackning=len(com) / len(ref), utanfor=(len(a) - len(com)) / len(a), spridning_sd=float(np.std(lr)),
                         spridning=float(1.4826 * np.median(np.abs(lr - np.median(lr))))))   # robust: viktbegränsade storbolag påverkar inte
R = pd.DataFrame(rows).merge(F[['q', 'fund_id', 'namn', 'bolag', 'jmf', 'B', 'namnindex', 'bred']], on=['q', 'fund_id'], how='left')
R['bred'] = R.bred.fillna(False).astype(bool); R['B'] = R.B.fillna(False).astype(bool); R['namnindex'] = R.namnindex.fillna(False).astype(bool)
R['regelA'] = (R.tackning >= 0.8) & (R.utanfor < 0.25) & (R.spridning < 0.45)
R['regelB'] = R.B & (R.bred | R.namnindex) & (R.tackning >= 0.6) & (R.spridning <= 0.7) & (R.utanfor <= 0.25)
R['omxsb_index'] = R.regelA | R.regelB
R['gammal_def'] = R.B & (R.bred | R.namnindex)
R.to_csv('agar_kontroll/indexfond_innehav.csv', index=False)
s = R.groupby('q').agg(ny=('omxsb_index', 'sum'), gammal=('gammal_def', 'sum'), tillkommer=('omxsb_index', lambda x: int((x & ~R.loc[x.index, 'gammal_def']).sum())),
                       faller_bort=('gammal_def', lambda x: int((x & ~R.loc[x.index, 'omxsb_index']).sum())))
print(s.to_string())
print('\nTillkommer någon gång:'); print(R[R.omxsb_index & ~R.gammal_def].groupby('namn').q.agg(['min', 'max', 'count']).to_string())
print('\nFaller bort någon gång:'); print(R[~R.omxsb_index & R.gammal_def].groupby('namn').q.agg(['min', 'max', 'count']).to_string())
