# T15 enligt runda5_deklaration.md (23:22). Återanvänder A/B-revisionens kod fram till händelsetabellen.
src = open('ab_revision.py').read().split("print('status per händelse:')")[0]
exec(src)
ok = D[(D.status == 'ok') & (D.n_placebo >= 20)].merge(fin[['event_id', 'AD', 'sister_member_before', 'sister_member_after', 'primär [AD-1,ED+1] indexslag']], on='event_id')
R_ = ok[(~ok.sister_member_before.astype(bool)) & (~ok.sister_member_after.astype(bool))]
def infer(sub):
    m = sub.spread.mean()
    nm = np.array([np.mean([rng.choice(pools[k]) for k in sub.event_id]) for _ in range(5000)])
    c = nm - nm.mean(); p = (np.abs(c) >= abs(m - nm.mean())).mean()
    return m, m - np.percentile(c, 97.5), m - np.percentile(c, 2.5), p
res = []
for lab, sub in [('systerslaget utanför index båda sidor, alla år', R_), ('samma, AD från 2017', R_[R_.AD >= '2017-01-01'])]:
    m, lo, hi, p = infer(sub); ixm = sub['primär [AD-1,ED+1] indexslag'].mean()
    res.append(dict(urval=lab, N=len(sub), bolag=sub.firm.nunique(), skattning=round(m, 2), ci_lo=round(lo, 2), ci_hi=round(hi, 2), p=round(p, 3),
                    indexslag_mot_marknaden=round(ixm, 2), övre_gräns_andel_av_indexslaget=round(hi / ixm, 2) if ixm > 0 else None))
R = pd.DataFrame(res); print(R.to_string(index=False))
import os; os.makedirs('runda5_resultat', exist_ok=True)
R.to_csv('runda5_resultat/T15_results.csv', index=False); R_.to_csv('runda5_resultat/T15_events.csv', index=False)
