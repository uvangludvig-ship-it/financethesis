"""Meaningful accounting counterexamples; no actual holdings are opened."""
import json
from run_overlap import bounds

def eq(actual,expected):
    assert max(abs(a-b) for a,b in zip(actual,expected)) < 1e-12

# A doubling in one fund cannot offset a complete exit in another.
eq(bounds([100,100],[100,100],[0,200],[1,1],[True,True])[:2],(.5,.5))
# An unobserved position retains its original denominator and [0,w] width.
eq(bounds([60,40],[60,float('nan')],[30,float('nan')],[1,float('nan')],[True,False])[:2],(.3,.7))
eq(bounds([60,40],[float('nan')]*2,[float('nan')]*2,[float('nan')]*2,[False,False])[:2],(0,1))
# Same economic quantity after 2-for-1 split is full endpoint overlap.
eq(bounds([100],[100],[200],[2],[True])[:2],(1,1))
# Split an identical position into two rows: result unchanged.
eq(bounds([25,75],[25,75],[10,30],[1,1],[True,True])[:2],(.4,.4))
eq(bounds([100],[100],[0],[1],[True])[:2],(0,0))
try:
    bounds([100],[100],[-1],[1],[True])
except AssertionError:
    pass
else:
    raise AssertionError('Negative source quantity accepted')
print(json.dumps({'synthetic_counterexamples_passed':7,'actual_q2_values_read':False}))
