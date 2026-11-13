# Kartläggning av OMXSB-följande fonder, 4 nov 2026 (plan: fondklassning_dd_plan.md). Körs mot staged filer.
# Steg 1: FI jämförelseindex; steg 2: FI handelsmönster per fond och år; steg 3: Lipper handelsmönster 2007–2026.
import pandas as pd, numpy as np, sys
U = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/financethesis'
H = pd.read_csv(f'{U}/data/derived/fi/fi_holdings_long.csv.gz', usecols=['Fond_institutnummer','Fond_namn','ISIN-kod_instrument','Antal','Kvartalsslut','Jämförelseindex','Fondförmögenhet'], low_memory=False)
H = H.rename(columns={'Fond_institutnummer':'fid','Fond_namn':'fnamn','ISIN-kod_instrument':'isin','Antal':'antal','Kvartalsslut':'q','Jämförelseindex':'jmf','Fondförmögenhet':'aum'})
H['q'] = pd.to_datetime(H.q); H['antal'] = pd.to_numeric(H.antal, errors='coerce')
# steg 1
pat = r'(?i)omx ?s(?:tockholm)? ?b(?:enchmark)?|omxsb|sbx|stockholm benchmark'
fq = H.groupby(['fid','q']).agg(fnamn=('fnamn','first'), jmf=('jmf','first'), aum=('aum','first')).reset_index()
fq['omxsb_jmf'] = fq.jmf.astype(str).str.contains(pat, regex=True)
cand = fq[fq.omxsb_jmf].groupby('fid').agg(namn=('fnamn','last'), forsta=('q','min'), sista=('q','max'), kvartal=('q','count'), jmf=('jmf', lambda s: ' | '.join(sorted(set(map(str, s)))))).reset_index()
cand.to_csv('steg1_fi_jmf_kandidater.csv', index=False)
# steg 2: träff per fond och år (ovillkorad: alla fonder som rapporterar båda kvartalen)
E = pd.read_csv(f'{U}/code/claude_checks/rattelser_2026-11-03_resultat/handelser_rattade.csv', parse_dates=['AD','ED'])
E['qb'] = pd.to_datetime(E.qb); E['qa'] = pd.to_datetime(E.qa); E = E[E.qb.notna() & E.qa.notna()]
P = H.groupby(['fid','q','isin']).antal.sum(); rep = H.groupby('q').fid.unique().to_dict(); rows = []
for r in E.itertuples():
    isins = [s for s in str(r.isins).split('|') if s and s != 'nan'] if isinstance(r.isins, str) else []
    if not isins and isinstance(r.isin, str): isins = [r.isin]
    for fid in set(rep.get(r.qb, [])) & set(rep.get(r.qa, [])):
        b = sum(P.get((fid, r.qb, i), 0) for i in isins); a = sum(P.get((fid, r.qa, i), 0) for i in isins)
        hit = int(b == 0 and a > 0) if r.type == 'addition' else int(b > 0 and a == 0)
        rows.append((fid, r.event_id, r.type, r.ED.year, hit))
T = pd.DataFrame(rows, columns=['fid','event_id','type','ar','hit'])
A = T[T.type == 'addition'].groupby(['fid','ar']).agg(n=('hit','size'), traff=('hit','mean')).reset_index()
T.groupby(['fid','ar']).agg(n=('hit','size'), traff=('hit','mean')).reset_index().to_csv('steg2_fi_traff_per_fond_ar.csv', index=False)
W = A[A.n >= 3].pivot(index='fid', columns='ar', values='traff').round(2); W['namn'] = W.index.map(H.groupby('fid').fnamn.last())
W[W.drop(columns='namn').max(axis=1) >= 0.4].to_csv('steg2_fi_tillagg_traff_matris.csv')
# steg 3: Lipper (villkorad: fonden finns bara för händelser där den ägde aktien i någon rapport)
F = pd.read_csv(f'{U}/code/claude_checks/data/runda8_fondagare.csv.gz', low_memory=False)
F = F.rename(columns={'Fund Name':'fond','Fund Shares Held (Adjusted)':'aktier','Fund Holdings Filing Date':'rapport','Fund Address Country':'land'})
F['rapport'] = pd.to_datetime(F.rapport, errors='coerce'); F['aktier'] = pd.to_numeric(F.aktier, errors='coerce')
I = pd.read_csv(f'{U}/code/claude_checks/runda8_input.csv', parse_dates=['AD','ED']); I = I[I.kind == 'event']
RD = F.dropna(subset=['rapport']).groupby('fond').rapport.apply(lambda s: np.sort(s.unique())).to_dict()
def reports(f, a, b):
    d = RD.get(f)
    if d is None: return False
    i = np.searchsorted(d, np.datetime64(a)); return i < len(d) and d[i] <= np.datetime64(b)
G = F.groupby(['event_id','fond','snap']).aktier.sum().unstack('snap').fillna(0).reset_index().merge(I[['event_id','type','AD','ED']], on='event_id')
G['ar'] = G.ED.dt.year
G = G[np.array([reports(f, a - pd.Timedelta(days=120), a - pd.Timedelta(days=1)) for f, a in zip(G.fond, G.AD)]) & np.array([reports(f, e, e + pd.Timedelta(days=45)) for f, e in zip(G.fond, G.ED)])]
G['hit'] = np.where(G.type == 'addition', (G.fore <= 0) & (G.efter > 0), (G.fore > 0) & (G.efter <= 0)).astype(int)
A = G[G.type == 'addition'].groupby(['fond','ar']).agg(n=('hit','size'), traff=('hit','mean')).reset_index()
W = A[A.n >= 3].pivot(index='fond', columns='ar', values='traff').round(2); W['max'] = W.max(axis=1); W['ar_over_0.5'] = (W.drop(columns='max') >= 0.5).sum(axis=1)
W['land'] = W.index.map(F.groupby('fond').land.first()); W.to_csv('steg3_lseg_tillagg_traff_matris.csv'); W[W['ar_over_0.5'] >= 2].to_csv('steg3_lseg_flaggade.csv')
