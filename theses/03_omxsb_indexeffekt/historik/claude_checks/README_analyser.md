# Två analyser som inte ligger i repot

Båda kördes i Claudes arbetsyta mot repot på commit b886f5b. Inget av detta är committat.

## 1. Fondgrupper per jämförelseindex (+0,21 / −0,21)

Skript: `parse_fi.py`, `split_others.py`

```
python3 parse_fi.py <repo>/data/raw/fi <repo>/output/omxsb_replication_2007/nettrading_omxsb.csv <utmapp>
python3 split_others.py <utmapp>/funds.csv <utmapp>/holdings.csv <repo>/output/omxsb_replication_2007/nettrading_omxsb.csv
```

- `parse_fi.py` läser alla FI-zipfiler (Fondinnehav_2018Q4 till 2026Q2) och skriver fondmetadata (`funds.csv`: jämförelseindex, aktiv risk, fondförmögenhet) samt innehav i händelseaktierna (`holdings.csv`).
- `split_others.py` klassar varje fond i förväg, utifrån jämförelseindex och aktiv risk, inte utifrån hur den handlade:
  - `tracker`: ensamt svenskt index med OMXSB och aktiv risk < 1,5 eller indexliknande namn
  - `bench_omxsb`: OMXSB någonstans i jämförelseindex, i övrigt aktiv eller blandfond
  - `other_swe_single`: annat ensamt svenskt index (SIX m.fl.)
  - `other`: övriga
- Mått: innehavsförändring kvartal före till kvartal efter, i procent av utestående aktier (`shares_qa`). Test: medel per översyn, t-test med G−1 frihetsgrader (15 översyner, 2019H1–2026H1).
- Utdata finns i `split_others_output.txt`. Raden `bench_omxsb` ger +0,209 (p 0,001) för tillägg och −0,209 (p 0,004) för borttag.
- Förbehåll: `bench_omxsb` innehåller även blandfonder med OMXSB som del av ett sammansatt index. Aktieantal är på bolagsnivå för A/B-aktier.

## 2. Lika långa fönster och väntetiden

Skript: `window_check.py`

```
python3 window_check.py <repo>/output/omxsb_replication_2007
```

- Del A läser repots `figures/fig_08_car_announcement.csv`. Kurvan är nollställd vid AD+10, så värdet vid dag −1 är −CAR[AD, AD+10]. Det är vanliga medelvärden per period, utan klustrat test.
- Del B läser `events_car.csv` och delar upp ann, mid (= tot − ann − eff) och eff före och efter Nasdaqs regeländring i maj 2021. Väntetiden föll då från 15 till 6–7 handelsdagar. Test: teckenbytesrandomisering på medel per översyn.
- Utdata finns i `window_check_output.txt`.

## Det som återstår (kräver aktiepanelen)

1. CAR per händelse i fasta fönster [AD, AD+5], [AD, AD+10] och [AD, AD+20], före och efter maj 2021, klustrat på översyn.
2. Daglig CAR från AD till ED+20 per regim: går den extra uppgången vid lång väntan tillbaka?
3. Samma sak för borttag.
