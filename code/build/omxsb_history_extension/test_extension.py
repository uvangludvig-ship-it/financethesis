"""Guard the historical-extension failure modes with small synthetic inputs."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

spec = importlib.util.spec_from_file_location("extension", Path(__file__).with_name("extend.py"))
extension = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extension)


class ExtensionTests(unittest.TestCase):
    def test_window_never_wraps_or_sums_partial_data(self):
        values = pd.Series([1., 2., np.nan, 4.])
        self.assertTrue(np.isnan(extension.complete_window(values, 0, -1, 1)))
        self.assertTrue(np.isnan(extension.complete_window(values, 3, 0, 1)))
        self.assertTrue(np.isnan(extension.complete_window(values, 0, 0, 2)))
        self.assertEqual(extension.complete_window(values, 0, 0, 1), 3.)

    def test_missing_price_does_not_create_multiday_one_day_return(self):
        dates = pd.bdate_range("2003-01-01", periods=4)
        px = pd.DataFrame(dict(ric="X.ST", date=dates, close=[100., np.nan, 110., 121.],
                               totret=np.nan, volume=10., bid=99., ask=101.))
        ix = pd.DataFrame(dict(ric=".OMXSBGI", date=dates, close=100.))
        _, series = extension.prepare_series(px, ix)
        self.assertTrue(np.isnan(series["X.ST"].ar.iloc[2]))
        self.assertAlmostEqual(series["X.ST"].ar.iloc[3], 10.)

    def test_supplement_cannot_replace_existing_data(self):
        old = pd.DataFrame(dict(ric=["X", "X"], date=["2003-01-01", "2003-01-02"], close=[100., np.nan]))
        new = pd.DataFrame(dict(ric=["X", "X"], date=["2003-01-01", "2003-01-02"], close=[999., 110.]))
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp)/"supp.csv"
            new.to_csv(file, index=False)
            result, overlaps = extension.merge_supplement(old, [file], ["ric", "date", "close"])
        self.assertEqual(result.close.tolist(), [100., 110.])
        self.assertEqual(overlaps[0]["close_nonmatching_nonmissing"], 1)

    def test_review_weighting_counts_reviews_not_stocks(self):
        frame = pd.DataFrame(dict(type=["addition"]*4, period=["2002–2006"]*4,
                                   review_cycle=["a", "a", "a", "b"], eff=[1., 1., 1., 5.]))
        row = extension.summarize(frame, ["eff"]).query("period == 'All' and type == 'addition'").iloc[0]
        self.assertEqual(row.events, 4)
        self.assertEqual(row.reviews, 2)
        self.assertEqual(row.mean_event, 2.)
        self.assertEqual(row.mean_review, 3.)
        self.assertLess(row.ci_low, 0.)

    def test_one_review_has_no_inferential_interval(self):
        frame = pd.DataFrame(dict(type=["deletion"]*2, period=["2002–2006"]*2,
                                   review_cycle=["a"]*2, eff=[1., 3.]))
        row = extension.summarize(frame, ["eff"]).query("period == 'All' and type == 'deletion'").iloc[0]
        self.assertTrue(np.isnan(row.ci_low))
        self.assertTrue(np.isnan(row.se_review))

    def test_missing_benchmark_session_stays_missing(self):
        dates = pd.bdate_range("2003-01-01", periods=4)
        px = pd.DataFrame(dict(ric="X.ST", date=dates, close=100., totret=1., volume=10., bid=99., ask=101.))
        ix = pd.concat([pd.DataFrame(dict(ric=".OMXSPI", date=dates, close=100.)),
                        pd.DataFrame(dict(ric=".OMXSBGI", date=dates, close=[100., np.nan, 110., 121.]))])
        cal, series = extension.prepare_series(px, ix)
        self.assertEqual(len(cal), 4)
        self.assertTrue(np.isnan(series["X.ST"].ar.iloc[1]))
        self.assertTrue(np.isnan(series["X.ST"].ar.iloc[2]))

    def test_unverified_price_seam_cannot_become_a_return(self):
        dates = pd.bdate_range("2003-01-01", periods=4)
        px = pd.DataFrame(dict(ric="X.ST", date=dates, close=[100., 101., 202., 204.],
                               close_source=["old", "old", "new", "new"],
                               totret=np.nan, volume=10., bid=99., ask=101.))
        ix = pd.DataFrame(dict(ric=".OMXSBGI", date=dates, close=100.))
        _, series = extension.prepare_series(px, ix)
        self.assertTrue(np.isnan(series["X.ST"].ar.iloc[2]))
        self.assertTrue(np.isfinite(series["X.ST"].ar.iloc[3]))

    def test_unverified_date_cannot_enable_announcement_outcomes(self):
        dates = pd.bdate_range("2002-01-01", "2004-01-01")
        px = pd.DataFrame(dict(ric="X.ST", date=dates, close=100., totret=1., volume=10., bid=99., ask=101.))
        ix = pd.DataFrame(dict(ric=".OMXSBGI", date=dates, close=100.))
        cal, series = extension.prepare_series(px, ix)
        event = dict(event_id="test", RIC="X.ST", type="addition", review_cycle="2003-01",
                     effective_date="2003-01-02", announcement_date="2002-12-20",
                     event_verified=False, ed_verified=False, ad_verified=False)
        measured, _ = extension.measure(event, cal, series)
        self.assertEqual(measured["eff"], 3.)
        self.assertTrue(np.isnan(measured["ann"]))
        self.assertTrue(np.isnan(measured["tot"]))


if __name__ == "__main__":
    unittest.main()
