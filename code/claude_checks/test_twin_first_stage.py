"""Regression checks for the legacy false-zero and stale-identifier failures."""
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("twin_first_stage", Path(__file__).with_name("twin_first_stage.py"))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class FirstStageGateTests(unittest.TestCase):
    def candidate(self):
        return {"event_id": "test", "AD": "2024-11-22", "usable_pair": "True",
                "sister_ric": "KINVa.ST", "sister_class": "A"}

    def test_kinnevik_override_is_date_specific(self):
        self.assertIsNone(gate.dated_sister_identifier("KINVa.ST", "A", "2024-06-06")["isin"])
        self.assertEqual(gate.dated_sister_identifier("KINVa.ST", "A", "2024-06-07")["isin"], "SE0022060513")
        self.assertIsNone(gate.dated_sister_identifier("KINVa.ST", "A", "")["isin"])
        self.assertIsNone(gate.dated_sister_identifier("KINVa.ST", "A", "2025-01-01")["isin"])

    def test_missing_endpoints_remain_missing_not_zero(self):
        row = gate.build_validation_rows([self.candidate()], {})[0]
        self.assertIn("snapshot_dates_missing_or_invalid", row["missing_inputs"])
        for field in gate.OUTCOME_FIELDS:
            self.assertIsNone(row[field])

    def test_known_identifier_does_not_validate_holdings(self):
        row = gate.build_validation_rows([self.candidate()],
            {"test": {"qb": "2024-09-30", "qa": "2024-12-31"}})[0]
        self.assertEqual(row["sister_isin_before"], "SE0022060513")
        self.assertEqual(row["status"], "blocked_not_an_economic_result")
        self.assertIsNone(row["sister_quantity_before"])

    def test_missing_files_write_explicit_blocked_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status = gate.audit(root / "absent_repo", root / "audit")
            self.assertFalse(status["legacy_0_74_pp_validated"])
            self.assertTrue(status["global_input_errors"])
            self.assertEqual(status["validated_economic_rows"], 0)
            self.assertTrue((root / "audit/first_stage_validation.json").exists())


if __name__ == "__main__":
    unittest.main()
