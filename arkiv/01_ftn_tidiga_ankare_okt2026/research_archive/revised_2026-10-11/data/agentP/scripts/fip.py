"""Company-level FIP = net flow-induced demand / market cap, for the largest names.
Market caps: stockanalysis.com Nasdaq Stockholm list, fetched 2026-10-11 (SEK bn, company level, both share classes same cap).
These are OCT-2026 caps, not event-date caps -> approximation. Names flagged approx=1 are my own rough caps (not on fetched list).
Usage: python -I fip.py <agentP_root>
"""
import sys, os, pandas as pd, numpy as np
P = sys.argv[1]; OUT = os.path.join(P, "out")
pd.set_option("display.width", 220); pd.set_option("display.max_rows", 200)

# isin -> (company, cap_bn_sek, approx_flag)
CAP = {
 "SE0000108656": ("Ericsson", 322, 0), "SE0000108649": ("Ericsson", 322, 0),
 "SE0017486897": ("Atlas Copco", 904, 0), "SE0017486889": ("Atlas Copco", 904, 0),
 "CH0012221716": ("ABB", 1640, 0), "SE0000107203": ("Industrivärden", 227, 0), "SE0000190126": ("Industrivärden", 227, 0),
 "SE0000115446": ("Volvo", 682, 0), "SE0000115420": ("Volvo", 682, 0), "SE0000148884": ("SEB", 443, 0), "SE0000120784": ("SEB", 443, 0),
 "SE0000242455": ("Swedbank", 440, 0), "SE0000667891": ("Sandvik", 461, 0), "SE0007100581": ("Assa Abloy", 379, 0),
 "SE0005190238": ("Tele2", 120, 0), "SE0005190246": ("Tele2", 120, 0), "SE0001174970": ("Millicom", 70, 1),
 "SE0000106270": ("H&M", 264, 0), "SE0009922164": ("Essity", 181, 0), "SE0009922156": ("Essity", 181, 0), "SE0011337708": ("AAK", 51, 0),
 "FI0009000681": ("Nokia", 542, 0), "SE0000202624": ("Getinge", 65, 0), "SE0014990966": ("Lagercrantz", 45, 0),
 "SE0000872095": ("Sobi", 156, 0), "SE0020050417": ("Boliden", 149, 0), "DK0010274414": ("Danske Bank", 300, 1),
 "SE0000163594": ("Securitas", 87, 0), "SE0015658109": ("Epiroc", 290, 0), "SE0015658117": ("Epiroc", 290, 0),
 "SE0000163628": ("Elekta", 21, 0), "SE0000667925": ("Telia", 184, 0), "SE0015811963": ("Investor", 1220, 0), "SE0015811955": ("Investor", 1220, 0),
 "SE0000375115": ("Mycronic", 62, 0), "SE0015192067": ("Nordnet", 85, 0), "FI0009013403": ("Kone", 300, 1),
 "SE0021921269": ("Saab", 309, 0), "SE0012673267": ("Evolution", 170, 0), "SE0012853455": ("EQT", 360, 0),
 "SE0000120669": ("SSAB", 103, 0), "SE0000171100": ("SSAB", 103, 0), "SE0001515552": ("Indutrade", 88, 0), "SE0014781795": ("Addtech", 86, 0),
 "SE0007100599": ("Handelsbanken", 302, 0), "SE0007100607": ("Handelsbanken", 302, 0), "SE0000114837": ("Trelleborg", 99, 0),
 "SE0000108847": ("Lundbergs", 143, 0), "SE0014504817": ("Loomis", 37, 0), "SE0015949748": ("Beijer Ref", 70, 0), "SE0015949201": ("Lifco", 138, 0),
 "SE0012454072": ("Avanza", 62, 0), "SE0000113250": ("Skanska", 109, 0), "SE0000695876": ("Alfa Laval", 221, 0), "SE0015961909": ("Hexagon", 252, 0),
 "GB0009895292": ("AstraZeneca", 2480, 0), "FI4000297767": ("Nordea", 673, 0), "SE0000108227": ("SKF", 120, 0), "SE0010100958": ("Latour", 130, 0),
 "SE0000112724": ("SCA", 95, 1), "SE0000171886": ("SCA", 95, 1), "SE0015988019": ("NIBE", 88, 0), "SE0000379190": ("Castellum", 57, 0),
 "SE0007074281": ("Hexpol", 33, 0), "SE0000382335": ("Autoliv", 86, 0), "SE0021628898": ("Volvo Car", 54, 1), "SE0006993770": ("Axfood", 54, 0),
 "FI4000552500": ("Sampo", 279, 0), "SE0000103814": ("Electrolux", 22, 0), "SE0001662230": ("Husqvarna", 21, 0), "SE0000164626": ("Sweco", 46, 1),
 "SE0011205202": ("Holmen", 49, 1), "SE0000109480": ("Holmen", 49, 1), "SE0018535619": ("Balder", 59, 1), "SE0000169991": ("Betsson", 13, 1),
 "SE0012673658": ("Sinch", 33, 0), "SE0000117970": ("Kinnevik", 17, 0), "SE0000113389": ("NCC", 18, 1), "SE0000101032": ("Peab", 28, 1),
 "SE0000106205": ("Bilia", 14, 1), "SE0000110165": ("Bravida", 29, 1), "SE0000163354": ("Sagax", 62, 1), "SE0017769532": ("Fabege", 22, 1),
 "SE0003366871": ("Wihlborgs", 23, 1), "SE0000124141": ("Munters", 25, 1), "SE0008294953": ("Thule", 22, 1), "SE0015658364": ("Storskogen", 19, 1),
 "SE0015812219": ("Embracer", 19, 1), "SE0012141687": ("Camurus", 35, 1), "SE0000122079": ("Billerud", 21, 1), "SE0000412367": ("Cloetta", 15, 1),
}
MONTHS = {"SE_active": 2, "SE_index_all": 9, "SE_index_exAvanzaZero": 4, "SE_index_AvanzaZeroOnly": 10, "Nordic_active": 3}

def company_level(tag, n_months, top=40):
    g = pd.read_csv(os.path.join(OUT, f"netdemand_{tag}.csv"), index_col=0)
    g["company"] = [CAP.get(i, (None,))[0] or i for i in g.index]
    g["cap_bn"] = [CAP.get(i, (None, np.nan))[1] for i in g.index]
    g["approx"] = [CAP.get(i, (None, np.nan, np.nan))[2] for i in g.index]
    c = g.groupby("company").agg(buy=("buy", "sum"), sell=("sell", "sum"), net=("net", "sum"), gross=("gross", "sum"),
                                  cap_bn=("cap_bn", "first"), approx=("approx", "first"), n_classes=("buy", "size"))
    c["fip_pct"] = 100 * c.net / (c.cap_bn * 1e9)
    c["fip_pct_per_tranche"] = c.fip_pct / n_months
    c["abs_net"] = c.net.abs()
    c = c.sort_values("abs_net", ascending=False)
    stats = dict(tag=tag, n_companies=len(c), sd_net_isin_m=g.net.std() / 1e6, sd_net_company_m=c.net.std() / 1e6,
                 top10_sq_share_company=(c.net ** 2).head(10).sum() / (c.net ** 2).sum(),
                 n_company_abs_net_gt_100m=int((c.net.abs() > 1e8).sum()),
                 n_mapped=int(c.cap_bn.notna().sum()), mapped_share_abs_net=c[c.cap_bn.notna()].abs_net.sum() / c.abs_net.sum(),
                 sd_fip_pct_mapped=c.fip_pct.std(), max_abs_fip_pct=c.fip_pct.abs().max(), n_abs_fip_gt_0p25=int((c.fip_pct.abs() > 0.25).sum()),
                 n_abs_fip_gt_0p10=int((c.fip_pct.abs() > 0.10).sum()), months_assumed=n_months)
    c.head(top).to_csv(os.path.join(OUT, f"fip_company_{tag}.csv"))
    return c, stats

S = []
for tag, nm in [("SE_active_2024q2_2024q2_equal_new", "SE_active"), ("SE_active_2024q2_2024q2_actual", "SE_active"), ("SE_active_2026q2_2026q2_actual", "SE_active"),
                ("SE_index_2026q2_2026q2_actual", "SE_index_all"), ("SE_index_2026q2_2026q2_actual_exAvanzaZero", "SE_index_exAvanzaZero"),
                ("SE_index_2026q2_2026q2_actual_AvanzaZeroOnly", "SE_index_AvanzaZeroOnly"), ("SE_index_2024q2_2026q2_actual", "SE_index_all"),
                ("Nordic_active_2024q2_2024q2_actual", "Nordic_active")]:
    c, st = company_level(tag, MONTHS[nm]); S.append(st)
    print(f"\n==== {tag}  (tranche months assumed {MONTHS[nm]})")
    print(c.head(25)[["net", "gross", "cap_bn", "approx", "fip_pct", "fip_pct_per_tranche", "n_classes"]].assign(net=lambda d: (d.net/1e6).round(0), gross=lambda d: (d.gross/1e6).round(0)).round(3).to_string())
pd.DataFrame(S).to_csv(os.path.join(OUT, "fip_summary.csv"), index=False)
print("\n", pd.DataFrame(S).round(3).to_string())
