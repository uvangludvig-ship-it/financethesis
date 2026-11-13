# T21 (runda6_deklaration.md, 10:40 CET): vilka fonder slutar äga efter borttag (uppdelning av T9 för borttag).
# Beskrivande, ej deklarerat. Samma urval, regression och inferens som T9/T14 (runda4.py).
# Körs från code/claude_checks:  python3 agar_kontroll/runda6_t21.py
# Kräver data/fi_all_holdings.pkl (byggs av fi_parse_all.py, ligger inte i git).
import sys, re, numpy as np, pandas as pd
sys.argv = ['x', '9']
src = open('runda4.py').read().split('# ---------- steg 0')[0]
exec(src)
F2 = pd.read_csv('data/fi_all_funds_klass.csv'); F2['fund_id'] = F2.fund_id.astype(str); F2['kv'] = pd.to_datetime(F2.kvartal)
F2 = F2.drop_duplicates(['kv', 'fund_id'], keep='last')
j = F2.jmf.fillna('').str.lower()
F2['B'] = j.str.contains(r'stockholm benchmark|omxsb|\bsbx')
F2['nameidx'] = F2.namn.astype(str).str.contains('index|indexnära|exponering|etf|xact|passiv|access', case=False, regex=True)
F2['bred'] = F2.bred.astype(bool)
F2['ar'] = pd.to_numeric(F2.aktiv_risk, errors='coerce')
INFO = F2.set_index(['kv', 'fund_id'])
cls = {k: v for k, v in zip(zip(F2.kv, F2.fund_id), F2[['B', 'nameidx', 'bred', 'ar', 'bolag']].itertuples(index=False))}
def cnt(owners, q, fn):
    return sum(1 for f in owners if (q, f) in cls and fn(cls[(q, f)]))
def comp(owners, q, fn=lambda c: True):
    return len({cls[(q, f)].bolag for f in owners if (q, f) in cls and fn(cls[(q, f)])})
defs = {
 'alla': lambda c: True,
 'B (OMXSB i jmf)': lambda c: c.B,
 'B, ej index i namnet': lambda c: c.B and not c.nameidx,
 'B, ej index i namnet, ej bred': lambda c: c.B and not c.nameidx and not c.bred,
 'B, aktiv risk > 1,5': lambda c: c.B and c.ar == c.ar and c.ar > 1.5,
 'ej B': lambda c: not c.B,
}
rows = []
for r in S.itertuples():
    d = {}
    if r.ok:
        h0 = HOLD.get((r.isn, r.q0), set()); h1 = HOLD.get((r.isn, r.q1), set())
        for k, fn in defs.items():
            d['n ' + k] = cnt(h1, r.q1, fn) - cnt(h0, r.q0, fn)
        d['bolag alla'] = comp(h1, r.q1) - comp(h0, r.q0)
        d['bolag B'] = comp(h1, r.q1, lambda c: c.B) - comp(h0, r.q0, lambda c: c.B)
        d['bolag ej B'] = comp(h1, r.q1, lambda c: not c.B) - comp(h0, r.q0, lambda c: not c.B)
        d['n h0'] = len(h0)
    rows.append(d)
S = pd.concat([S, pd.DataFrame(rows)], axis=1)
q = S[(S.type == 'deletion') & S.ok]
print('Borttag med data:', int(q.event.sum()), ' kontroller:', int((q.event == 0).sum()), ' översyner:', q.review.nunique())
out = []
for c in [c for c in S.columns if c.startswith('n ') and c != 'n h0'] + ['bolag alla', 'bolag B', 'bolag ej B']:
    rr = reg(q, q[c]); out.append(dict(utfall=c, **rr)); print(f'{c:35s}', fmt(rr))
pd.DataFrame(out).to_csv('agar_kontroll/T21_results.csv', index=False)
# vilka fonder: nya B-ägare bland tillägg, per fondbolag
new = []
for r in S[(S.type == 'deletion') & (S.event == 1) & S.ok].itertuples():
    h0 = HOLD.get((r.isn, r.q0), set()); h1 = HOLD.get((r.isn, r.q1), set())
    for f in h0 - h1:
        c = cls.get((r.q0, f))
        if c is not None and c.B: new.append(dict(ric=r.ric, review=r.review, fund=f, namn=INFO.loc[(r.q0, f), 'namn'], bolag=c.bolag, nameidx=c.nameidx, bred=c.bred, ar=c.ar))
N = pd.DataFrame(new); N.to_csv('agar_kontroll/T21_tappade_B_agare.csv', index=False)
print('\nTappade B-ägare per borttag i snitt:', round(len(N) / q.event.sum(), 2))
print(N.groupby('bolag').size().sort_values(ascending=False).head(12))
print(N.groupby(['bolag', 'namn']).size().sort_values(ascending=False).head(25))
