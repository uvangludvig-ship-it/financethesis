"""READY BUT NOT RUN: paste into the user's existing Workspace CodeBook.

Source/access pilot only. Nine bounded data calls; no return or trading outcomes.
TR field names below are attested in LSEG's own documentation/community replies.
Their availability on this exact index/account is tested, never assumed.
Outputs are licensed local exports: do not publish the raw CSVs.

LSEG RIC .OMXSBPI was verified by live LSEG IndexQuotes metadata on 2026-11-03.
The earlier project candidate .OMXSB failed resolution and remains in logs.
Nasdaq's separate display symbol is OMXSBPI. A label mismatch stops interpretation, not an
automatic switch to the capped .OMXSBCAPGI or any ETF proxy.
"""
import pandas as pd
import json
try:
    import lseg.data as ld
except ImportError:
    import refinitiv.data as ld

INDEX = '.OMXSBPI'
DATES = ['2023-11-30', '2023-12-01']
FIELDS = [
    'TR.IndexConstituentName',
    'TR.IndexConstituentWeightPercent',
    'TR.IndexConstituentShares',
    'TR.IndexConstituentWeightPercent.date',
]
FIELD_SOURCES = {
    'core': 'https://community.developers.lseg.com/discussion/105781/retrieving-historical-constituent-data-using-r/p1',
    'weight_date': 'https://community.developers.lseg.com/discussion/65797/constituent-list-and-weight-for-spx-using-python-api',
}
ledger = []
ld.open_session()  # Existing authenticated CodeBook session; no supplied key.

def fetch(label, fields, parameters):
    row = {'label': label, 'index': INDEX, 'fields': fields,
           'parameters': parameters, 'utc': pd.Timestamp.now(tz='UTC').isoformat()}
    try:
        df = ld.get_data(universe=[INDEX], fields=fields, parameters=parameters)
        if df is None:
            row.update(status='no_dataframe')
        else:
            filename = 'index_pilot_' + label + '.csv'
            df.to_csv(filename, index=False)
            row.update(status='response_requires_validation', file=filename,
                       rows=len(df), columns=[str(c) for c in df.columns],
                       nonnull_counts={str(c): int(df[c].notna().sum()) for c in df.columns},
                       nonempty_counts={str(c):int((df[c].notna()&df[c].astype(str).str.strip().ne('')).sum())for c in df.columns})
    except Exception as exc:
        # Do not replace unavailable fields/dates by a different concept or today.
        row.update(status='field_or_content_error', exception=type(exc).__name__,
                   message=str(exc)[:500])
    ledger.append(row)
    pd.DataFrame(ledger).to_json('index_pilot_request_log.json', orient='records', indent=2)
    print(label, row['status'], row.get('rows', ''), row.get('columns', ''))

# Current label only, never used as a historical constituent observation.
fetch('index_identity', ['TR.InstrumentName'], {})

# Probe each field independently so one invalid field cannot erase all results.
# RIC is an alignment key; errors and blank values remain explicit failures.
for day in DATES:
    for number, field in enumerate(FIELDS, 1):
        fetch(day.replace('-', '') + '_field' + str(number),
              ['TR.IndexConstituentRIC', field], {'SDate': day.replace('-', '')})

print('SOURCE PILOT ONLY. Check index identity, historical returned date, field')
print('definitions, complete membership, and whether weights are SOD or EOD.')
print('No official Nasdaq original-file/vintage claim follows from a vendor response.')
print('Weight differences across two trading dates include price drift; do not test them.')
