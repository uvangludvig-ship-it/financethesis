# Hela kurspanelen för Stockholmsbörsen (LSEG), alla aktier med RIC som innehåller .ST, handelsdagarna i OMXSBGI:s kalender.
# Läses av steg 11 till 13 med exec (DATA och cal definieras där). Panelen ligger i tre filer för att varje fil ska vara under 50 MB.
import pandas as pd
PANELFILER = ['all_stocks_daily_2004_2012.csv.gz', 'all_stocks_daily_2013_2019.csv.gz', 'all_stocks_daily_2020_2026.csv.gz']
px = pd.concat([pd.read_csv(DATA / 'prices' / f, parse_dates=['date']) for f in PANELFILER], ignore_index=True)
px = px[px.date.isin(cal)].sort_values(['ric', 'date']).reset_index(drop=True)
