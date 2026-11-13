"""Build source-verification overlays. Reads only candidate identity/date metadata.

No returns, price files, API sessions or workbook writes. Run with bundled Python.
Public overlay contains row references and audit labels, not vendor issuer/RIC data.
"""
from pathlib import Path
from collections import Counter
import csv, datetime, hashlib, json

BASE = Path(__file__).resolve().parent

def dump(name, obj):
    (BASE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

def write_csv(name, records):
    with (BASE / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0]))
        w.writeheader()
        w.writerows(records)

def main():
    candidates = list(csv.DictReader((BASE / "private/CANDIDATE_METADATA.csv").open()))
    assert len(candidates) == 57
    assert len({r['workbook_row'] for r in candidates}) == 57
    counts = Counter((r['candidate_ED'], r['type']) for r in candidates)
    dates = sorted({r['candidate_ED'] for r in candidates})
    assert dates == json.loads((BASE / "SCOPE_LOCK.json").read_text())['candidate_dates']
    reviews = []
    events = []
    for date in dates:
        review_id = f"CANDIDATE-{date}"
        reviews.append(dict(
            review_id=review_id,
            candidate_effective_date=date,
            candidate_date_source="user workbook L&J, Date column; not independently verified",
            candidate_additions=counts[(date, 'addition')],
            candidate_deletions=counts[(date, 'deletion')],
            announcement_date="",
            announcement_time="",
            announcement_timezone="",
            effective_date="",
            effective_date_convention="UNVERIFIED: do not assume previous close, opening, calendar Jan 1 or first trading day",
            announcement_verified=False,
            effective_date_verified=False,
            full_change_list_verified=False,
            review_verified=False,
            source_url="",
            source_evidence="",
            corrections_checked="NO_ORIGINAL_NOTICE_FOUND",
            status="MISSING_PRIMARY_REVIEW_NOTICE",
            missing_reason="Bounded public-source search did not locate the SBX/OMXSB review notice or issuer confirmation. No AD inferred."
        ))
    for r in sorted(candidates, key=lambda x: int(x['workbook_row'])):
        events.append(dict(
            workbook_row=int(r['workbook_row']),
            review_id=f"CANDIDATE-{r['candidate_ED']}",
            candidate_effective_date=r['candidate_ED'],
            announcement_date="",
            effective_date="",
            event_verified=False,
            issuer_verified_from_notice=False,
            share_class_verified_from_notice=False,
            direction_verified_from_notice=False,
            source_url="",
            evidence="No original review/issuer notice found; workbook issuer labels may be modern. This row is not verified for AD-based analysis."
        ))
    write_csv("REVIEW_VERIFICATION.csv", reviews)
    write_csv("EVENT_VERIFICATION_OVERLAY.csv", events)
    dump("VALIDATION.json", dict(
        checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        candidate_reviews=len(reviews), candidate_events=len(events),
        candidate_additions=sum(counts[(d,'addition')] for d in dates),
        candidate_deletions=sum(counts[(d,'deletion')] for d in dates),
        verified_reviews=0, verified_events=0,
        announcement_dates_filled=0, primary_effective_dates_filled=0,
        seed_rows_in_overlay=0,
        public_overlay_vendor_issuer_and_ric_columns=False,
        interpretation="Zero verified in this search is missing evidence, not zero true reviews/events or proof originals do not exist.",
        pass_checks=["8 expected candidate dates", "57 unique workbook rows", "no initial 2002 seed rows", "no guessed AD or ED", "no raw issuer/RIC in public overlay"]
    ))

if __name__ == '__main__':
    main()
