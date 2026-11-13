"""Diagnostics on the notebook's actual holdings intermediates. No FTN events."""
import json
import numpy as np
import pandas as pd

def run(ns, out):
    e, h, idx = ns["e5"], ns["h"], ns["IDX"]
    b, a, pres = ns["own_b"], ns["own_a"], ns["pres"]
    meta = h.groupby(["Fond_institutnummer", "Kvartalsslut"], as_index=False).agg(
        fund_name=("Fond_namn", "last"), manager=("Fondbolag_namn", "last"),
        fund_isin=("Fond_ISIN-kod", "last"), benchmark=("Jämförelseindex", "last"))
    meta["anchor_trade_classifier"] = meta.Fond_institutnummer.isin(idx)
    meta["reported_omxsb_benchmark"] = meta.benchmark.fillna("").str.contains(
        r"OMX.?SB|Stockholm Benchmark|\bSBX\b", case=False, regex=True)
    meta["name_or_manager_changed"] = meta.groupby("Fond_institutnummer").fund_name.transform("nunique").gt(1) | meta.groupby("Fond_institutnummer").manager.transform("nunique").gt(1)
    meta[meta.anchor_trade_classifier].to_csv(out/"tracker_quarter_metadata.csv", index=False)
    lookup = meta.set_index(["Fond_institutnummer", "Kvartalsslut"])
    records, detail = [], []
    for r in e.itertuples():
        both = pres[r.qb] & pres[r.qa]
        rec = dict(event_id=r.event_id, company=r.company, type=r.type, AD=r.AD, ED=r.ED,
                   qb=r.qb, qa=r.qa, denominator=r.shares_qa, split_proxy=r.f,
                   n_report_b=len(pres[r.qb]), n_report_a=len(pres[r.qa]), n_report_both=len(both),
                   n_report_enter=len(pres[r.qa]-pres[r.qb]), n_report_exit=len(pres[r.qb]-pres[r.qa]))
        for ids, col in [(idx,"nt"), (set(ns["funds"].index),"instbuy"), (set(ns["funds"].index)-idx,"activebuy")]:
            raw_b = b[r.event_id].loc[b[r.event_id].index.isin(ids)].sum()*r.f
            raw_a = a[r.event_id].loc[a[r.event_id].index.isin(ids)].sum()
            rec[col+"_unpaired"] = 100*(raw_a-raw_b)/r.shares_qa
            rec[col+"_paired"] = getattr(r,col)
        # Subset restriction is diagnostic, not a replacement tracker definition:
        # contemporaneously reported OMXSB-related benchmark at both endpoints.
        mandate_ids = {f for f in both & idx if bool(lookup.loc[(f,r.qb),"reported_omxsb_benchmark"]) and bool(lookup.loc[(f,r.qa),"reported_omxsb_benchmark"])}
        rec["n_reported_benchmark_subset"] = len(mandate_ids)
        rec["nt_reported_benchmark_subset"] = 100*(a[r.event_id].loc[a[r.event_id].index.isin(mandate_ids)].sum()-r.f*b[r.event_id].loc[b[r.event_id].index.isin(mandate_ids)].sum())/r.shares_qa
        rec["identity_residual"] = r.instbuy-r.nt-r.activebuy
        for f in set(b[r.event_id].index) | set(a[r.event_id].index):
            pb, pa = f in pres[r.qb], f in pres[r.qa]
            if pb and pa:
                status = "paired_reporter"
            else:
                status = "missing_report_after" if pb else "missing_report_before"
            detail.append(dict(event_id=r.event_id, fund=f, qb=r.qb, qa=r.qa,
                status=status, anchor_tracker=f in idx,
                quantity_before_adjusted=b[r.event_id].get(f,0)*r.f if pb else np.nan,
                quantity_after=a[r.event_id].get(f,0) if pa else np.nan,
                delta= a[r.event_id].get(f,0)-b[r.event_id].get(f,0)*r.f if pb and pa else np.nan))
        records.append(rec)
    diag=pd.DataFrame(records)
    diag.to_csv(out/"holdings_measurement_audit.csv",index=False)
    detail=pd.DataFrame(detail)
    detail.to_csv(out/"event_fund_reporting.csv.gz",index=False,compression="gzip")
    # Candidate transfer links: same fund-ISIN under different institution IDs.
    # These are flags for verification; no transfer is inferred or netted away.
    links=meta.dropna(subset=["fund_isin"])
    ids=links.groupby("fund_isin").Fond_institutnummer.nunique()
    links[links.fund_isin.isin(ids[ids>1].index)].to_csv(out/"possible_fund_id_transfers.csv",index=False)
    ns["nmchk"].to_csv(out/"historical_isin_name_flags.csv",index=False)
    chk=ns["chk"].copy()
    chk["price_ratio_flag"] = (~chk.fi_vs_lseg_b.between(.8,1.2)) | (~chk.fi_vs_lseg_a.between(.8,1.2))
    chk["split_needs_source"] = chk.f.ne(1)
    chk.to_csv(out/"split_denominator_checks.csv",index=False)
    # Carry source ambiguity as flags; never discard an extreme return.
    nameflags=set(ns["nmchk"].loc[ns["nmchk"].flag,"event_id"])
    diag["unresolved_name_link"] = diag.event_id.isin(nameflags)
    diag["unverified_split"] = diag.split_proxy.ne(1)
    diag["price_ratio_flag"] = diag.event_id.map(chk.set_index("event_id").price_ratio_flag)
    diag["measurement_screen"] = ~(diag.unresolved_name_link | diag.unverified_split | diag.price_ratio_flag)
    diag.to_csv(out/"holdings_measurement_audit.csv",index=False)
    # Detect alternate share classes whose reported LSEG denominator is identical.
    mc, sh=ns["mcw"],ns["shw"]
    denominators=[]
    for ric1,ric2 in [("VOLVa.ST","VOLVb.ST"),("SSABa.ST","SSABb.ST"),("ATCOa.ST","ATCOb.ST")]:
        if ric1 in sh and ric2 in sh:
            z=pd.DataFrame({"a":sh[ric1],"b":sh[ric2]}).dropna()
            cap=pd.DataFrame({"a":mc[ric1],"b":mc[ric2]}).dropna()
            denominators.append(dict(ric_a=ric1,ric_b=ric2,days=len(z),same_shares_fraction=float(np.isclose(z.a,z.b).mean()),
                mcap_days=len(cap),same_mcap_fraction=float(np.isclose(cap.a,cap.b).mean())))
    pd.DataFrame(denominators).to_csv(out/"shareclass_denominator_diagnostics.csv",index=False)
    summary=dict(events=len(e),reviews=e.AD.nunique(),max_identity_error=float(diag.identity_residual.abs().max()),
        changed_unpaired_to_paired={v:int((abs(diag[v+"_unpaired"]-diag[v+"_paired"])>1e-10).sum()) for v in ["nt","instbuy","activebuy"]},
        events_with_name_flags=len(nameflags),events_with_split_proxy=int(chk.split_needs_source.sum()),
        price_ratio_flags=int(chk.price_ratio_flag.sum()), screened_events=int(diag.measurement_screen.sum()),
        transfer_candidate_isins=int((ids>1).sum()),
        tracker_quarters_without_reported_benchmark=int((meta.anchor_trade_classifier & ~meta.reported_omxsb_benchmark).sum()))
    (out/"holdings_audit_summary.json").write_text(json.dumps(summary,indent=2))
    print("HOLDINGS AUDIT",summary)
