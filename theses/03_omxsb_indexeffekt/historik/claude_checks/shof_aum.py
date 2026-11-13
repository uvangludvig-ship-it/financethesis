# OMXSB-fondernas förmögenhet per månad ur SHoF Valuations (data/shof/shof_valuations_2026-11-02.zip).
# Rättelse 2 nov 18:10: den första serien (tracker_aum_shof.csv, utan skript) använde bara tnafund, som saknas för
# Swedbank Robur Access Sverige och Access Edge Sweden 2025-01 till 2026-08. Där blev förmögenheten 0.
# Nu: dagsvärde = tnafund, annars summan av tnaclass för fondens andelsklasser i listan samma dag; månadsvärde = senaste
# dagsvärde inom 92 dagar före månadens slut (SHoF saknar ibland hela månader för en fond).
# Körs från code/claude_checks: python3 shof_aum.py  ->  data/shof/tracker_aum_shof_v2.csv
import os, zipfile
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'data', 'shof')
L = pd.read_csv(os.path.join(D, 'shof_fondlista.csv'))
with zipfile.ZipFile(os.path.join(D, 'shof_valuations_2026-11-02.zip')) as z:
    V = pd.read_csv(z.open(z.namelist()[0]), sep=';', parse_dates=['date'], usecols=['performanceId', 'date', 'tnaclass', 'tnafund'])
V = V.merge(L[['performanceid', 'fundid', 'fundname']].drop_duplicates(), left_on='performanceId', right_on='performanceid')
V['m'] = V.date.dt.to_period('M')

def fond_manad(x):   # en fund id: dagsvärde = tnafund, annars summan av tnaclass samma dag; månadsvärde = senaste dagsvärde inom 92 dagar före månadens slut
    f = x.dropna(subset=['tnafund']).groupby('date').tnafund.last()
    c = x.dropna(subset=['tnaclass']).groupby('date').tnaclass.sum()
    dag = pd.concat([f.rename('v').to_frame().assign(kalla='tnafund'), c[~c.index.isin(f.index)].rename('v').to_frame().assign(kalla='tnaclass')]).sort_index()
    out = {}
    for m in pd.period_range('2006-01', V.m.max(), freq='M'):
        slut = m.to_timestamp(how='end'); d = dag[(dag.index <= slut) & (dag.index > slut - pd.Timedelta(days=92))]
        out[m] = (d.v.iloc[-1], d.kalla.iloc[-1]) if len(d) else (float('nan'), 'saknas')
    return pd.DataFrame(out, index=['v', 'kalla']).T

namn = {'Nordea Indexfond Sverige': None, 'Nordea Inst Aktie Sverige': None, 'Swedbank Robur Access Sverige': None,
        'Nordnet Indexfond Sverige ESG': None, 'Öhman Marknad Sverige': None, 'Swedbank Robur Access Edge Sweden': None,
        'Länsförsäkringar Sverige Index': '2025-06', 'Storebrand Sverige': '2025-10'}   # värde: månad då fonden börjar följa OMXSB
xact = 'XACT Sverige (UCITS ETF)'   # följde OMXSB (som XACT OMXSB) t.o.m. 2018-12
idx = pd.period_range('2006-01', V.m.max(), freq='M'); res = pd.DataFrame(index=idx); kalla = pd.DataFrame(index=idx)
for fn in list(namn) + [xact]:
    parts = [fond_manad(x) for _, x in V[V.fundname == fn].groupby('fundid')]
    v = sum(p.v.astype(float).reindex(idx).fillna(0) for p in parts) / 1e9
    k = parts[0].kalla.reindex(idx) if len(parts) == 1 else pd.concat([p.kalla for p in parts], axis=1).reindex(idx).astype(str).agg('/'.join, axis=1)
    res[fn] = v; kalla[fn] = k
alla = sum(res[fn].where((idx >= pd.Period(st, 'M')) if st else [True] * len(idx), 0) for fn, st in namn.items())
out = pd.DataFrame({'manad': idx.astype(str), 'omxsb_foljare_mdkr': alla.values,
                    'inkl_xact_omxsb_mdkr': (alla + res[xact].where(idx <= pd.Period('2018-12', 'M'), 0)).values})
for fn in res: out['fond: ' + fn] = res[fn].values
for fn in kalla: out['källa: ' + fn] = kalla[fn].values
out.to_csv(os.path.join(D, 'tracker_aum_shof_v2.csv'), index=False)
gam = pd.read_csv(os.path.join(D, 'tracker_aum_shof.csv'))
j = out.merge(gam[['manad', 'shof_inkl_xact_omxsb_mdkr']], on='manad')
j['diff'] = j.inkl_xact_omxsb_mdkr - j.shof_inkl_xact_omxsb_mdkr
print('månader där v2 skiljer sig från första serien med mer än 0,05 mdkr:', int((j['diff'].abs() > 0.05).sum()))
print(j[j['diff'].abs() > 0.05][['manad', 'shof_inkl_xact_omxsb_mdkr', 'inkl_xact_omxsb_mdkr', 'diff']].round(1).to_string(index=False))
print(out[out.manad.str.endswith('-12') | (out.manad == out.manad.max())][['manad', 'omxsb_foljare_mdkr', 'inkl_xact_omxsb_mdkr']].round(1).to_string(index=False))
