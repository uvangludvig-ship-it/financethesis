# Hela kurspanelen uppställd som i runda 3 (code/claude_checks/runda3.py, 1 nov 2026), för steg 12 och 13.
# Läses med exec efter att 01:s huvud har körts (DATA, cal, pos, mkt, np, pd finns då).
# Skillnader mot panel.py: Nordea och Tieto tas från LSEG:s separata hämtning, dagsavkastningar över 1 000 % stryks,
# börsvärdet fylls framåt högst 10 dagar.
import re
exec(open(DATA.parent / 'code' / 'panel.py', encoding='utf-8').read())
px = px[['ric', 'date', 'close', 'totret', 'volume', 'mcap', 'shares', 'bid', 'ask']]
_S = pd.read_csv(DATA / 'prices' / 'nordea_tieto_daily_lseg.csv', low_memory=False); _add = []
for _r in ['NDASE.ST', 'TIETOS.ST']:
    _d = _S[(_S.ric == _r) & _S.Date.notna()].copy(); _d['date'] = pd.to_datetime(_d.Date)
    _m = _S[(_S.ric == _r) & (_S.typ == 'marknadsvarde_manad')].reset_index(drop=True)
    _m['date'] = pd.date_range('2006-01-31', periods=len(_m), freq='ME')   # antagande från runda 3: jan 2006 till okt 2026 i ordning
    _d = _d.merge(_m[['date', 'Outstanding Shares']].rename(columns={'Outstanding Shares': 'shares'}), on='date', how='outer').sort_values('date')
    _d['shares'] = _d.shares.ffill(); _d = _d[_d.TRDPRC_1.notna()]
    _add.append(pd.DataFrame(dict(ric=_r, date=_d.date, close=_d.TRDPRC_1, totret=np.nan, volume=_d.ACVOL_UNS, mcap=_d.TRDPRC_1 * _d.shares, shares=_d.shares, bid=_d.BID, ask=_d.ASK)))
px = pd.concat([px[~px.ric.isin(['NDASE.ST', 'TIETOS.ST'])]] + _add, ignore_index=True)
px = px[px.date.isin(cal)].drop_duplicates(['ric', 'date'], keep='last').sort_values(['ric', 'date'])
def nextpos(d):
    d = pd.Timestamp(d); i = cal.searchsorted(d); return int(i) if i < len(cal) else None
def _rser(gr):
    gr = gr.set_index('date'); r = gr.totret.fillna(gr.close.pct_change() * 100)
    return r.reindex(cal[(cal >= gr.index.min()) & (cal <= gr.index.max())])
RET = pd.DataFrame({r: _rser(gr) for r, gr in px.groupby('ric')}).reindex(cal); RET = RET.mask(RET > 1000)
AR3 = RET.sub(mkt, axis=0); CI = {r: i for i, r in enumerate(AR3.columns)}; _A = AR3.values
_CS = np.vstack([np.zeros(_A.shape[1]), np.nancumsum(_A, axis=0)]); _CN = np.vstack([np.zeros(_A.shape[1]), np.cumsum(np.isnan(_A), axis=0)])
def wsum3(ric, a, b):
    if ric not in CI or a is None or b is None or pd.isna(a) or pd.isna(b): return np.nan
    a = int(a); b = int(b)
    if a < 0 or b >= len(cal): return np.nan
    j = CI[ric]; return np.nan if _CN[b + 1, j] - _CN[a, j] > 0 else _CS[b + 1, j] - _CS[a, j]
_piv = lambda c: px.pivot_table(index='date', columns='ric', values=c).reindex(cal)
CLOSE = _piv('close'); mc = _piv('mcap').ffill(limit=10); VOL = _piv('volume'); SH = _piv('shares'); TV = VOL * CLOSE
def root(r):
    m = re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST', str(r)); return m.group(1) if m else str(r)
