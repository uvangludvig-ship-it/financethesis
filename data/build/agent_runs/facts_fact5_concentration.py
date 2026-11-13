"""FACT 5: fund-company concentration (top-5 forvaltare share) and Swedish-managed share in procured sub-categories at award vs +12m (or latest)."""
from common import *
d = load_panel(); t1, t2 = load_rounds()
END = d.date.max()
rows = []
for rd, Ame in AWARD_ME.items():
    A = pd.Timestamp(Ame); B = min(A + pd.offsets.MonthEnd(12), END)
    M = t1[t1['round'] == rd]
    inc = M[M.role != 'winner_new'].fondnr.tolist(); allf = M.fondnr.tolist()
    kat = M.kategori.mode().iloc[0]
    for lab, dt, fl in [('award', A, inc), ('after', B, allf)]:
        x = d[(d.date == dt) & d.fondnr.isin(fl)]
        tot = x.mv_tot.sum()
        g = x.groupby('forvaltare').mv_tot.sum().sort_values(ascending=False)
        top5 = 100 * g.head(5).sum() / tot; top1 = 100 * g.iloc[0] / tot
        hhi = ((100 * g / tot) ** 2).sum()
        sv = 100 * x[x.svensk == 'Svensk'].mv_tot.sum() / tot
        rows.append(dict(round=rd, universe='procured_subcategory', when=lab, date=dt.date(), n_funds=len(x), n_companies=len(g), cap_bn=tot / 1e9, top1_pct=top1, top1=g.index[0], top5_pct=top5, hhi=hhi, swedish_pct=sv,
                         top5=';'.join(g.head(5).index)))
    # whole panel category
    for lab, dt in [('award', A), ('after', B)]:
        x = d[(d.date == dt) & (d.kategori == kat)]
        if len(x) == 0: continue
        tot = x.mv_tot.sum(); g = x.groupby('forvaltare').mv_tot.sum().sort_values(ascending=False)
        rows.append(dict(round=rd, universe='panel_kategori:' + kat, when=lab, date=dt.date(), n_funds=len(x), n_companies=len(g), cap_bn=tot / 1e9, top1_pct=100 * g.iloc[0] / tot, top1=g.index[0],
                         top5_pct=100 * g.head(5).sum() / tot, hhi=((100 * g / tot) ** 2).sum(), swedish_pct=100 * x[x.svensk == 'Svensk'].mv_tot.sum() / tot, top5=';'.join(g.head(5).index)))
C = pd.DataFrame(rows)
C.to_csv(O + 'fact5_concentration.csv', index=False)
piv = C[C.universe == 'procured_subcategory'].pivot(index='round', columns='when', values=['n_funds', 'n_companies', 'cap_bn', 'top1_pct', 'top5_pct', 'hhi', 'swedish_pct'])
print(piv.round(1).to_string())
piv2 = C[C.universe != 'procured_subcategory'].pivot(index='round', columns='when', values=['n_funds', 'n_companies', 'cap_bn', 'top5_pct', 'hhi', 'swedish_pct'])
print(piv2.round(1).to_string())
print(C[C.universe == 'procured_subcategory'][['round', 'when', 'top1', 'top5']].to_string())
# pooled across executed rounds (capital-weighted)
E = C[(C.universe == 'procured_subcategory')]
for w in ['award', 'after']:
    z = E[E.when == w]
    print(w, 'cap-weighted mean top5', round(np.average(z.top5_pct, weights=z.cap_bn), 1), 'swedish', round(np.average(z.swedish_pct, weights=z.cap_bn), 1), 'hhi', round(np.average(z.hhi, weights=z.cap_bn)), 'n_funds', z.n_funds.sum(), 'n_companies', z.n_companies.sum())
