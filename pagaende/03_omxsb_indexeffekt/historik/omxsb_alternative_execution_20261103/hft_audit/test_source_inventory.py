"""Synthetic source-format counterexamples, never real licensed values."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest, zipfile, gzip
from inspect_hft_source import inspect

class SourceInventoryTests(unittest.TestCase):
    def test_missing_exact_duplicates_and_semicolon_quotes(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parent) as d:
            p=Path(d)/'synthetic.zip'
            content='time;phase;quote;note\n09:00:00;T;;"one;two"\n09:00:00;T;;"one;two"\n09:01:00;A;N/A;x\n09:01:00;A;0;x\n'
            with zipfile.ZipFile(p,'w') as z:z.writestr('synthetic.csv',content)
            x=inspect(p,['phase'])['members'][0]
            self.assertEqual(x['row_count'],4)
            self.assertEqual(x['exact_duplicate_rows'],1)
            self.assertEqual(x['missing_count']['quote'],3)
            self.assertEqual(x['explicit_categorical_counts']['phase'],{'T':2,'A':2})
            self.assertEqual(x['malformed_rows'],0)
    def test_same_timestamp_different_rows_not_collapsed(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parent) as d:
            p=Path(d)/'synthetic.csv';p.write_text('time,match,status\n1,123,trade\n1,123,cancel\n')
            x=inspect(p,['status'])['members'][0]
            self.assertEqual(x['row_count'],2)
            self.assertEqual(x['exact_duplicate_rows'],0)
            self.assertEqual(x['explicit_categorical_counts']['status'],{'trade':1,'cancel':1})
    def test_gzip_content_with_zip_suffix(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parent) as d:
            p=Path(d)/'synthetic.csv.zip'
            with gzip.open(p,'wt') as f:f.write('time;status\n08:45:00;IOO\n')
            x=inspect(p,['status'])['members'][0]
            self.assertEqual(x['row_count'],1)
            self.assertEqual(x['columns'],['time','status'])

if __name__=='__main__':unittest.main()
