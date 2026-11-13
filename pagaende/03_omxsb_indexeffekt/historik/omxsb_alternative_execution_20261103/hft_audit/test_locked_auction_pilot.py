"""Synthetic tests of ambiguity/missingness/direction failure modes, no market data."""
import unittest
import pandas as pd
from execute_locked_auction_pilot import select_quote,auction_price,premium,signed_contrast,clock_check

class GateTests(unittest.TestCase):
    def book(self):
        return pd.DataFrame({'date':['2023-11-23']*3,
         'time':['08:45:00.100000000','09:00:01.000000000','17:24:59.000000000'],
         'status':['IOO','IOO','T'],'bidpx1':['99']*3,'askpx1':['101']*3,
         'bidsz1':['5']*3,'asksz1':['7']*3})
    def test_conflicting_last_timestamp_blocks(self):
        x=self.book(); y=x.iloc[[-1]].copy();y['askpx1']='102';x=pd.concat([x,y],ignore_index=True)
        with self.assertRaisesRegex(ValueError,'ambiguous'):select_quote(x)
    def test_missing_auction_never_uses_last_trade(self):
        x=pd.DataFrame({'Date':['2023-11-23'],'CLS_AUC':[None],'CLS_AUCVOL':[100],'TRDPRC_1':[100]})
        with self.assertRaisesRegex(ValueError,'auction_field'):auction_price(x,'2023-11-23')
    def test_local_vs_utc_phase_discrimination(self):
        x=self.book()
        self.assertTrue(clock_check(x,'exchange_local')['passes'])
        self.assertFalse(clock_check(x,'UTC')['passes'])
    def test_direction_sign_and_basis_points(self):
        ap=premium(101,100); base=premium(100,100)
        self.assertAlmostEqual(ap,100)
        self.assertAlmostEqual(signed_contrast(1,base,ap),100)
        self.assertAlmostEqual(signed_contrast(-1,base,ap),-100)
    def test_quote_after_call_never_selected(self):
        x=self.book();x.loc[2,'time']='17:25:00.000000000'
        with self.assertRaisesRegex(ValueError,'no_valid_quote'):select_quote(x)

if __name__=='__main__':unittest.main(verbosity=2)
