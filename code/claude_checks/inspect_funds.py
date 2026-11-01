import csv, sys, re, collections
F = list(csv.DictReader(open(sys.argv[1])))
def fl(x):
    try: return float(x.replace(',','.'))
    except: return None
# funds with Swedish broad benchmarks
pat = re.compile(r'stockholm benchmark|omxsb|six return|sixrx|six portfolio|omx stockholm|omxs|msci sweden|solactive sweden|morningstar sweden|vinx|sverige', re.I)
rows = [r for r in F if r['quarter']=='2024-06-30' and pat.search(r['benchmark'] or '')]
rows.sort(key=lambda r: -(fl(r['aum']) or 0))
print('2024Q2 funds with Swedish benchmarks:', len(rows))
for r in rows[:45]:
    print(f"{(fl(r['aum']) or 0)/1e9:7.1f} bn  AR={r['active_risk']:>5}  {r['fund_name'][:42]:42s} | {r['benchmark'][:60]}")
