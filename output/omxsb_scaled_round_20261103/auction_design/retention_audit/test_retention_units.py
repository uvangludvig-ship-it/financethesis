import unittest
from reconstruct_retention import level,paired

class UnitTests(unittest.TestCase):
 def test_physical_split_does_not_create_retention_change(self):
  self.assertEqual(level(20,2,10,1000),level(60,6,10,1000))
 def test_missing_or_negative_quantity_never_zero(self):
  for v in [float('nan'),-1]:
   with self.assertRaises(ValueError):level(v,1,10,1000)
 def test_missing_control_not_reweighted(self):
  with self.assertRaises(ValueError):paired({'event':1,'c1':0,'c2':0})
  self.assertAlmostEqual(paired({'event':1,'c1':0,'c2':.3,'c3':.6}),.7)

if __name__=='__main__':unittest.main(verbosity=2)
