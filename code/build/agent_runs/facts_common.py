import pandas as pd, numpy as np
S = '/tmp/claude-0/-home-claude/5b447583-b5ae-51ff-a30e-274749b6d7af/scratchpad/'
F = S + 'ftn/'
O = S + 'fresh/facts/'
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 60); pd.set_option('display.max_rows', 400)

def load_panel():
    d = pd.read_csv(F + 'ppm_panel_2018_2026.csv', parse_dates=['date'], low_memory=False)
    d = d[~d.fondnr.isin([1, 2, 3, 4]) & ~d.fondnamn.str.contains('AP7', na=False)].copy()
    d = d.drop_duplicates(['fondnr', 'date']).sort_values(['fondnr', 'date'])
    d['mv_lag'] = d.groupby('fondnr').mv_tot.shift()
    d['val_lag'] = d.groupby('fondnr').val_tot.shift()
    d['is_dec'] = d.date.dt.month == 12
    return d

def load_rounds():
    t1 = pd.read_csv(F + 'agentA/task1_round_membership.csv', parse_dates=['award', 'first_month', 'last_month'])
    t2 = pd.read_csv(F + 'agentA/task2_loser_decomposition.csv', parse_dates=['last_month', 'move_start'])
    return t1, t2

# award month-end per executed round (panel month in which award falls)
AWARD_ME = {'EU_active': '2024-03-31', 'EU_index': '2024-10-31', 'Global_index': '2024-10-31', 'Nordic_active': '2025-02-28',
            'Nordic_smallcap': '2025-02-28', 'SE_active': '2025-08-31', 'SE_index': '2025-08-31', 'EU_smallcap': '2026-05-31',
            'SE_smallcap': '2026-05-31'}

# Global active round (award 2026-02-24, appealed, no move by 2026-08): FTN report sec 4.1 (45 incumbents at 31 Dec 2025) matched to panel
GA_INCUMBENTS = {
    273839: 'Allianz Global Equity Growth AT', 878694: 'Allianz Global Water AT', 309666: 'Allianz Pet and Animal Wellbeing AT',
    908277: 'AMF Aktiefond Global', 645952: 'AMF Aktiefond Världen', 791863: 'Amundi Global Equity Conservative A2',
    294322: 'AXA IM Global Equity QI B (left PPM Oct 2025)', 118000: 'BL - Equities Dividend B', 320358: 'BL - Global Equities B',
    515554: 'C WorldWide Global Equities 1A', 479725: 'C WorldWide Global Equities Ethical 1A', 541235: 'D&G Global All Cap',
    366154: 'CPR Invest Global Lifestyles A2', 793109: 'Evli Global Placeringsfonden B', 202002: 'Fondita Global Megatrends B',
    717496: 'Franklin Mutual Global Discovery A', 123679: 'Handelsbanken Global Tema A1', 282632: 'Holberg Global A',
    271478: 'Indecap Guide 2 C', 152835: 'Lärarfond Offensiv', 964767: 'Öhman/Lannebo Global A', 163923: 'Öhman Global Growth A',
    563965: 'Länsförsäkringar Global Vision A', 282517: 'Nordea Global', 562421: 'Odin Global C', 912691: 'Pareto Global B',
    690693: 'Pictet Global Megatrend Selection R', 923383: 'Pictet Premium Brands R', 968891: 'Pictet Security R',
    301580: 'SEB Aktiesparfond', 520759: 'SEB Dynamisk Aktiefond', 698952: 'SEB Global Aktiefond',
    479550: 'Seligson & Co Global Top 25 Brands A', 475301: 'Skandia Världen', 465147: 'Spiltan Globalfond Investmentbolag',
    184580: 'Delphi Global A2', 153007: 'SKAGEN Focus D', 984187: 'SKAGEN Global E', 201111: 'GodFond Sverige & Världen',
    912220: 'Storebrand Global High Dividend Low Volatility A', 162099: 'Storebrand Global Multifactor A',
    941096: 'Folksam LO Världen', 785022: 'Swedbank Robur Aktiefond Pension', 422709: 'BMC Global Select Fund',
    989491: 'Ålandsbanken Global Aktie B Placeringsfond'}
# FTN report sec 5.5: 14 winners, of which 6 incumbents
GA_WINNERS_INC = [908277, 541235, 698952, 941096, 785022, 989491]
GA_AWARD_ME = pd.Timestamp('2026-02-28')
