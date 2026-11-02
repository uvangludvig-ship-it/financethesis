"""Correct the exported demand labels without rerunning or altering any estimates."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from omxsb_demand_labels import demand_labels

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "output/omxsb_audit_20261031"
OUT = ROOT / "output/omxsb_extension_20261031/labels"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [AUDIT / "result_table.csv", AUDIT / "corrected/mechanisms/results_table_long.csv"]
    before_hash = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    old = pd.read_csv(paths[0])
    new = old.copy(deep=True)
    source = pd.read_csv(paths[1])
    selected = source[source.explanation.str.startswith("Demand (") & source["sample"].eq("all")]
    changes = []
    seen = set()
    for row in selected.to_dict("records"):
        typ = "addition" if ", additions," in row["test"] else "deletion"
        matches = old.index[
            old.question.eq("Prisreaktion och trackerhandel") & old.type.eq(typ)
            & old.N.eq(row["N"]) & old.independent_reviews.eq(row["G"])
            & np.isclose(old.estimate, row["coef"], rtol=1e-12, atol=1e-12)
        ]
        if len(matches) != 1 or int(matches[0]) in seen:
            raise ValueError(f"Nonunique source-to-summary match: {row['test']}")
        i = int(matches[0]); seen.add(i)
        for field, value in demand_labels(row["test"]).items():
            if old.loc[i, field] != value:
                changes.append(dict(row=i, field=field, before=old.loc[i, field], after=value,
                                    source_test=row["test"]))
                new.loc[i, field] = value
    numeric = old.select_dtypes("number").columns
    pd.testing.assert_frame_equal(old[numeric], new[numeric], check_exact=True)
    change_table = pd.DataFrame(changes)
    assert change_table.row.nunique() == 8
    assert len(selected) == 10
    new.to_csv(OUT / "result_table_labels_corrected.csv", index=False)
    change_table.to_csv(OUT / "label_changes.csv", index=False)
    view = new[["question", "type", "period", "window", "unit", "estimate", "ci_low", "ci_high", "N", "independent_reviews"]]
    (OUT / "RESULTATTABELL.md").write_text(
        "# Rättade resultatetiketter\n\nÅtta rader har rättade etiketter, perioder, enheter och tolkningar. "
        "Samtliga numeriska resultat är oförändrade från omkörningen i omxsb_audit_20261031. "
        "Ingen ny skattning görs här. Källvägarna i CSV avser den ursprungliga auditkatalogen.\n\n"
        + view.to_markdown(index=False, floatfmt=".3f") + "\n"
    )
    after_hash = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    assert before_hash == after_hash
    validation = dict(rows=len(new), source_demand_rows=len(selected), relabeled_rows=8,
                      numeric_results_unchanged=True, original_inputs_unchanged=True,
                      input_sha256=before_hash)
    (OUT / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2))
    print(json.dumps(validation, ensure_ascii=False))


if __name__ == "__main__":
    main()
