"""
lseg_codebook_pull.py: pull the stock panel for thesis 2 inside LSEG Workspace CodeBook.

How to use
  1. Workspace -> search "CodeBook" -> open it -> New -> Python 3 notebook (or upload this file and open it).
  2. Run STEP 0 alone first. If it prints a small table for Investor B, the field names work.
     If it errors on a field, comment that field out in FIELDS and tell Claude the error text.
  3. Run STEP 1 (universe), then STEP 2 (prices; runs in chunks, can take 1 to 3 hours, safe to restart:
     finished chunks are skipped), then STEP 3 (static), STEP 4 (indices).
  4. Zip the folder 'thesis_data' (right-click in the CodeBook file browser -> Download) and put the files in
     ~/Documents/financethesis_fresh/thesis2/data/prices/

Nothing here touches returns around FTN dates; it only downloads raw data.
"""
import os, time
import pandas as pd
import lseg.data as ld          # in older CodeBook images: import refinitiv.data as ld

OUT = "thesis_data"; os.makedirs(OUT, exist_ok=True); os.makedirs(f"{OUT}/chunks", exist_ok=True)
START, END = "2005-01-01", pd.Timestamp.today().strftime("%Y-%m-%d")

FIELDS = [
    "TR.PriceClose",            # close price (adjusted for splits)
    "TR.TotalReturn",           # daily total return in % (dividends included)
    "TR.Volume",                # shares traded
    "TR.TurnoverValue",         # value traded in local currency (if this errors, drop it; we use price x volume)
    "TR.CompanyMarketCap",      # market cap
    "TR.SharesOutstanding",     # shares outstanding
]

ld.open_session()

# ---------------------------------------------------------------- STEP 0: test on one stock
test = ld.get_history(universe=["INVEb.ST"], fields=FIELDS, start="2024-05-01", end="2024-05-20", interval="daily")
print(test)

# ---------------------------------------------------------------- STEP 1: universe (active AND delisted)
# Stockholm main market (XSTO), First North Sweden (FNSE), Spotlight (SSME); delisted RICs carry a ^ suffix.
screen = ('SCREEN(U(IN(Equity(active,inactive,public,primary))), '
          'IN(TR.ExchangeMarketIdCode,"XSTO","FNSE","SSME"), CURN=SEK)')
uni = ld.get_data(universe=screen, fields=["TR.CommonName", "TR.ISIN", "TR.ExchangeMarketIdCode", "TR.InstrumentIsActive"])
uni.to_csv(f"{OUT}/universe.csv", index=False)
rics = uni["Instrument"].dropna().unique().tolist()
print(len(rics), "instruments;", uni["TR.InstrumentIsActive" if "TR.InstrumentIsActive" in uni else uni.columns[-1]].value_counts())
# Sanity check: expect well over 1,000 instruments, a large share of them inactive. If you get only a few hundred,
# the screen dropped delisted names; tell Claude.

# ---------------------------------------------------------------- STEP 2: daily history in chunks
def pull_chunk(batch, i):
    path = f"{OUT}/chunks/prices_{i:04d}.csv"
    if os.path.exists(path):
        return
    for attempt in range(3):
        try:
            df = ld.get_history(universe=batch, fields=FIELDS, start=START, end=END, interval="daily")
            df.to_csv(path)
            return
        except Exception as e:
            print("chunk", i, "attempt", attempt, e); time.sleep(10)

BATCH = 25
for i in range(0, len(rics), BATCH):
    pull_chunk(rics[i:i + BATCH], i // BATCH)
    if (i // BATCH) % 10 == 0:
        print("done chunk", i // BATCH, "of", len(rics) // BATCH)

# stack the wide chunks into one long file: id, date, field values
longs = []
for f in sorted(os.listdir(f"{OUT}/chunks")):
    w = pd.read_csv(f"{OUT}/chunks/{f}", header=[0, 1], index_col=0)
    l = w.stack(level=0).reset_index()
    l.columns = ["date", "id"] + list(l.columns[2:])
    longs.append(l)
pd.concat(longs).to_csv(f"{OUT}/stocks_daily.csv", index=False)

# ---------------------------------------------------------------- STEP 3: static fields
static = ld.get_data(universe=rics, fields=["TR.CommonName", "TR.ISIN", "TR.TickerSymbol", "TR.ExchangeMarketIdCode",
                                            "TR.TRBCEconomicSector", "TR.TRBCIndustryGroup", "TR.FirstTradeDate",
                                            "TR.RetireDate", "TR.FreeFloatPct"])
static.to_csv(f"{OUT}/stocks_static.csv", index=False)

# ---------------------------------------------------------------- STEP 4: indices
IDX = [".OMXS30", ".OMXSPI", ".OMXSB", ".OMXSBGI", ".OMXSBCAPGI", ".SIXPRX", ".SIX30RX"]
for r in IDX:
    try:
        h = ld.get_history(universe=[r], fields=["TR.PriceClose"], start=START, end=END, interval="daily")
        h.to_csv(f"{OUT}/index_{r.strip('.')}.csv")
        print(r, len(h))
    except Exception as e:
        print(r, "not found:", e)   # tell Claude which ones fail; there are alternative codes

ld.close_session()
print("finished; download the folder", OUT)
