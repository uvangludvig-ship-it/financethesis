"""Synthetic aggregation counterexamples; no licensed data."""
import unittest
import pandas as pd
from validate_sampled_export import compare

class SamplingTests(unittest.TestCase):
 def full(self):
  return pd.DataFrame({'time':['09:01:01','09:01:58','17:24:01','17:24:59'],
   'date':['2023-11-23']*4,'status':['T']*4,'_source_member':['synthetic']*4,
   'bidpx1':['99','100','101','103'],'askpx1':['101','102','103','105'],
   'bidsz1':['5']*4,'asksz1':['6']*4})
 def test_last_original_time_is_equivalent(self):
  x=self.full();s=x.iloc[[1,3]].reset_index(drop=True)
  z=compare(x,s,60)
  self.assertTrue(z['coherent_last_snapshot_terminal_equivalence'])
  self.assertTrue(z['source_supported_original_freshness'])
 def test_mean_price_is_not_last_quote(self):
  x=self.full();s=x.iloc[[0,2]].reset_index(drop=True)
  s['time']=['09:01:00','17:24:00'];s['bidpx1']=['99.5','102'];s['askpx1']=['101.5','104']
  z=compare(x,s,60)
  self.assertFalse(z['coherent_last_snapshot_terminal_equivalence'])
  self.assertTrue(any(c['aggregation']=='arithmetic_snapshot_mean' and c['all_compared_rows_match'] for c in z['candidates']))
 def test_end_label_does_not_invent_update_time(self):
  x=self.full();s=x.iloc[[1,3]].reset_index(drop=True);s['time']=['09:02:00','17:25:00']
  z=compare(x,s,60)
  self.assertTrue(z['coherent_last_snapshot_terminal_equivalence'])
  self.assertFalse(z['source_supported_original_freshness'])
  self.assertTrue(z['requires_explicit_bin_label_or_carry_forward_assessment'])
 def test_missing_intermediate_quote_is_preserved_not_zero(self):
  x=self.full();x.loc[1,'bidpx1']='N/A';s=x.iloc[[1,3]].reset_index(drop=True)
  self.assertTrue(compare(x,s,60)['coherent_last_snapshot_terminal_equivalence'])
  s.loc[0,'bidpx1']='0'
  self.assertFalse(compare(x,s,60)['coherent_last_snapshot_terminal_equivalence'])

if __name__=='__main__':unittest.main(verbosity=2)
