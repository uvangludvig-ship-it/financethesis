"""Independent numerical and selection invariants for the control-analysis repair."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
import statsmodels.api as sm

spec=importlib.util.spec_from_file_location('repair',Path(__file__).with_name('robusthet_hela.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class RepairTests(unittest.TestCase):
    def test_cluster_estimates_against_statsmodels(self):
        rng=np.random.default_rng(704)
        groups=np.repeat(np.arange(8),[3,9,2,8,4,7,5,6])
        x=rng.normal(size=len(groups));X=np.column_stack([np.ones(len(x)),x])
        y=.7+1.9*x+rng.normal(size=8)[groups]+rng.normal(size=len(x))
        actual=m.cluster_fit(X,y,groups)
        reference=sm.OLS(y,X).fit(cov_type='cluster',cov_kwds={'groups':groups,'use_correction':True})
        np.testing.assert_allclose(actual['coef'],reference.params,atol=1e-12)
        np.testing.assert_allclose(actual['se'],reference.bse,atol=1e-12)

    def test_fast_wild_equals_explicit_refits(self):
        rng=np.random.default_rng(34)
        groups=np.repeat(np.arange(5),[4,7,3,8,6]);x=rng.normal(size=len(groups))
        X=np.column_stack([x,np.ones(len(x))]);y=.2*x+2+rng.normal(size=5)[groups]+rng.normal(size=len(x))
        B,label,j=199,'independent-refit',0
        actual=m.wild_cluster_p(X,y,groups,j,B,label)
        fit=m.cluster_fit(X,y,groups)
        fr=np.full(len(y),y.mean());er=y-fr
        W=m.rng_for(('wild',label)).choice(m.WEBB,(B,5))
        tsim=[]
        for w in W:
            f=m.cluster_fit(X,fr+er*w[groups],groups)
            tsim.append(f['coef'][j]/f['se'][j])
        expected=m.tail_p(tsim,fit['coef'][j]/fit['se'][j])
        self.assertEqual(actual,expected)

    def test_unequal_cluster_sizes_do_not_change_review_estimand(self):
        y=[1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,9.,-2.]
        groups=['a']*10+['b','c']
        ans=m.mean_inference(y,groups,B=199,label='weights')
        compressed=m.mean_inference([1.,9.,-2.],['a','b','c'],B=199,label='weights')
        self.assertAlmostEqual(ans['estimate_pp'],8/3)
        for key in ['estimate_pp','ci_lo','ci_hi','p_signflip','p_wild']:
            self.assertAlmostEqual(ans[key],compressed[key])
        self.assertNotAlmostEqual(ans['estimate_pp'],ans['event_weighted_mean_pp'])

    def test_ties_and_finite_simulation_correction(self):
        self.assertEqual(m.tail_p([1.,-1.],1.+1e-15,exact=True),1.)
        self.assertEqual(m.tail_p([0.,0.],10.),1/3)
        self.assertEqual(m.signflip_means([0.,0.,0.]),1.)

    def test_no_predictor_outcome_overlap(self):
        w=m.window_bounds(200,220)
        self.assertEqual(w['pre_end']-w['pre_start']+1,100)
        self.assertLess(w['pre_end'],w['outcome_start'])
        self.assertLess(w['covariate_day'],w['outcome_start'])

    def test_future_events_do_not_select_controls(self):
        self.assertFalse(m.past_or_current_event('XYZ.ST',3,{('XYZ.ST',4)}))
        self.assertTrue(m.past_or_current_event('XYZ.ST',3,{('XYZ.ST',2)}))
        self.assertTrue(m.past_or_current_event('XYZ.ST',3,{('XYZ.ST',3)}))

    def pool(self):
        return pd.DataFrame(dict(ric=['AAa.ST','AAb.ST','BBa.ST','BBb.ST','CC.ST','DD.ST'],
                                 issuer=['AA','AA','BB','BB','CC','DD'],
                                 precar=[0.,.01,.1,.11,.3,.7],log_mcap=[2.,2.,2.,2.,3.,4.],
                                 car=[1.,2.,3.,4.,np.nan,6.]))

    def test_distinct_issuers_and_no_outcome_selection(self):
        pool=self.pool();event=dict(issuer='AA',precar=.1,log_mcap=2.)
        mu=pool[['precar','log_mcap']].mean();sd=pool[['precar','log_mcap']].std()
        chosen=m.choose_matches(pool,event,mu,sd)
        self.assertEqual(list(chosen.issuer),['BB','CC','DD'])
        modified=pool.copy();modified['car']=[np.nan]*6
        self.assertEqual(list(chosen.ric),list(m.choose_matches(modified,event,mu,sd).ric))
        self.assertTrue(np.isnan(m.paired_difference(2.,chosen.car,3)))
        self.assertAlmostEqual(m.paired_difference(2.,chosen.car,1),-1.)

    def test_not_enough_valid_issuers_never_selects_sibling(self):
        pool=self.pool().iloc[:4];event=dict(issuer='AA',precar=0.,log_mcap=2.)
        chosen=m.choose_matches(pool,event,pd.Series({'precar':0.,'log_mcap':0.}),pd.Series({'precar':1.,'log_mcap':1.}))
        self.assertEqual(len(chosen),1)
        self.assertTrue(np.isnan(m.paired_difference(2.,chosen.car,3)))

    def test_same_supported_reviews(self):
        d=pd.DataFrame({'review':['a','a','b','c','c'],'event':[0,1,1,0,1],
                        'precar':[0.,1.,9.,10.,11.],'log_mcap':[2.,2.,2.,2.,2.]})
        s=m.supported_reviews(d)
        self.assertEqual(set(s.review),{'a','c'})
        self.assertTrue(m.common_support(d).empty)

    def test_issuer_proxy_handles_dead_ric_and_classes(self):
        self.assertEqual(m.issuer_key('SSABa.ST'),m.issuer_key('SSABb.ST'))
        self.assertEqual(m.issuer_key('KLOVa.ST^D22'),m.issuer_key('KLOVb.ST^D22'))
        self.assertNotEqual(m.issuer_key('AB.ST'),m.issuer_key('ABC.ST'))


if __name__=='__main__':
    unittest.main(verbosity=2)
