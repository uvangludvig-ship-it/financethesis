import os, json
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "output", "omxsb_replication_2007")
SL = os.path.join(REPO, "slides")
WIN = {"ann": "Announcement [AD−1, AD+1]", "eff": "Effective [ED−1, ED+1]", "tot": "Total [AD−1, ED+1]"}

t = pd.read_csv(os.path.join(OUT, "tables", "tab_02_car_long.csv"))
PER = [p for p in t.period.drop_duplicates() if p not in ("diff", "F_equal")]  # the notebook's periods, in order
t = t[t.period.isin(PER)]

def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""

def block(typ, win):
    s = t[(t.type == typ) & (t.window == win)].set_index("period").reindex(PER)
    m = " & ".join(f"{r['mean']:.2f}{stars(r.p_hc1)}" for _, r in s.iterrows())
    se = " & ".join(f"({r.se_hc1:.2f})" for _, r in s.iterrows())
    pw = " & ".join(f"\\{{{r.p_wcb:.2f}\\}}" for _, r in s.iterrows())
    n = " & ".join(f"{int(r.N)}" for _, r in s.iterrows())
    return m, se, pw, n

head = "\\begin{tabular}{l" + "r" * len(PER) + "}\n\\toprule\n & " + " & ".join(PER) + " \\\\\n\\midrule\n"
tail = "\\bottomrule\n\\end{tabular}\n"

rows = []
for typ, lab in [("addition", "Additions"), ("deletion", "Deletions")]:
    m, se, pw, n = block(typ, "tot")
    rows.append(f"\\textbf{{{lab}}} & {m} \\\\\n & {se} \\\\\n & {pw} \\\\\n$N$ & {n} \\\\")
open(os.path.join(SL, "tab02_total.tex"), "w").write(head + "\n\\addlinespace\n".join(rows) + "\n" + tail)

rows = []
for typ, lab in [("addition", "Additions"), ("deletion", "Deletions")]:
    for win in ["ann", "eff", "tot"]:
        m, se, pw, n = block(typ, win)
        rows.append(f"{lab}, {WIN[win].split(' ')[0].lower()} & {m} \\\\\n & {se} \\\\\n & {pw} \\\\")
open(os.path.join(SL, "tab02_all.tex"), "w").write(head + "\n\\addlinespace\n".join(rows) + "\n" + tail)

num = json.load(open(os.path.join(OUT, "mechanisms", "numbers_mechanisms.json")))
keys = [k for k in num if k.startswith("fig3_")]
print({k: num[k] for k in keys})
print("wrote", os.path.join(SL, "tab02_total.tex"), "and tab02_all.tex")
