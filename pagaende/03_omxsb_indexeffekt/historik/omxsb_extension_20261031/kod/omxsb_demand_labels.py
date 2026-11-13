"""Preserve the distinct variables, units and periods of the demand regressions."""
import re


def demand_labels(test):
    period_match = re.search(r", (\d{4})-(\d{4})$", test)
    if not period_match:
        raise ValueError(f"Demand regression lacks a source period: {test}")
    period = "–".join(period_match.groups())
    if test.startswith("total return on net trading by OMXSB trackers,"):
        return dict(
            question="Prisreaktion och trackerhandel", period=period,
            window="AD−1:ED+1 mot kvartalsförändring", unit="pp CAR per 1% aktier",
            supports="Samvariation mellan två observerade mått",
            does_not_support="Ingen kausal elasticitet; kvartalsförändring omfattar annan handel",
        )
    if test.startswith("total return on expected demand, % of mcap"):
        return dict(
            question="Prisreaktion och beräknad efterfrågan, andel av marknadsvärde",
            period=period, window="AD−1:ED+1 mot AUM / rekonstruerad OMXSB-kapitalisering före AD",
            unit="pp CAR per procentenhet beräknad efterfrågan/marknadsvärde",
            supports="Samvariation mellan CAR och beräknad efterfrågan; variation mellan översyner",
            does_not_support="Inte observerad handel eller kausal elasticitet; samma efterfrågeandel för alla aktier inom översynen",
        )
    if test.startswith("total return on expected demand in days of ADV,"):
        return dict(
            question="Prisreaktion och beräknad efterfrågan, dagar av ADV",
            period=period, window="AD−1:ED+1 mot AUM × beräknad indexvikt / ADV före AD",
            unit="pp CAR per dag av genomsnittlig handelsomsättning (ADV)",
            supports="Samvariation mellan CAR och beräknad efterfrågan relativt handelsomsättning",
            does_not_support="Inte observerad handel eller kausal elasticitet; måttet beror på omsättning och rekonstruerade indexvikter",
        )
    raise ValueError(f"Unrecognized demand regression: {test}")
