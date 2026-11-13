"""Assemble technical research records; never generates thesis prose."""
from pathlib import Path
import json,hashlib,shutil,zipfile
import pandas as pd
R=Path('/Users/ludviguvang/dev/financethesis')
C=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke')
O=R/'output/omxsb_broadening_20261102'
D=R/'code/build/omxsb_broadening_20261102'
U=C/'outputs'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def finish():
    s=pd.read_csv(O/'switchers/results.csv').set_index('model').loc['primary_pre_balance']
    m=pd.read_csv(O/'models/model_scores.csv')
    sh=json.loads((O/'short_positions/RESULTS.json').read_text())
    b=sh['equal_review_mean_identification_bounds'];n=pd.read_csv(O/'frontier/network_baseline_coverage.csv')
    text=f'''OMXSB — AVGRÄNSAD BREDDNING, 2 NOVEMBER 2026
Teknisk forsknings- och beslutssammanställning. Inte uppsatstext.

VAD SOM FORTFARANDE ÄR ÖPPET
Först: hur mycket av den relativa prisrörelsen orsakas av indexinträdet, snarare
än av att Nasdaq väljer aktier med andra framtidsutsikter? Sedan: vilka kanaler
förmedlar en eventuell kausal effekt — exempelvis mandatstyrda köp eller ökad
uppmärksamhet? Kanalerna kan verka tillsammans. Separat är varaktigheten efter
20 dagar fortfarande osäkert skattad. Inget av testen nedan stänger dessa frågor.

DENNA RUNDA: TRE NYA UTFALLSANALYSER OCH EN NY DATAGRANSKNING
Tidigare ägardecomposition, retention, prisfönster, AP, volym och mandatgranskning
räknas inte som nya resultat här. Ingen uttömmande lista över alla tänkbara
ekonomiska hypoteser påstås. Samtliga försök och osäkra resultat bevaras.

1. SAMMA AKTIER VID TILLÄGG OCH BORTTAG — GENOMFÖRT
{int(s.N)} händelser, {int(s.securities)} aktieslag, {int(s.issuers)} bolag, {int(s.reviews)} översyner.
Samma tidigare matchningar/fönster, aktie- och översynseffekter, kontroll för
föravkastnings- och storleksobalans. Tillägg-minus-borttag: {s.estimate_pp:.3f}
procentenheter. Reviewklustrat 95%-intervall [{s.review_ci_low:.3f}; {s.review_ci_high:.3f}],
tvåvägs bolag/review [{s.two_way_ci_low:.3f}; {s.two_way_ci_high:.3f}]. Wild-p {s.p_wild_review:.4f}
gäller reviewproceduren och ersätter inte de bredare osäkerhetsmåtten.
Beslut: kompletterande robusthetskontroll som tar bort stabila aktieskillnader,
men har stor osäkerhet och kvarstående tidsvarierande urval. Ingen ny
kausal mekanism. Två fasta modeller, inga nya fönster eller periodgrids.
Källa: switchers/REPORT.txt, results.csv, validation.json, REPLAY_VALIDATION.json.

2. PRIS OCH TVÅ MÅTT PÅ FONDKÖP — GENOMFÖRT
Gemensamt urval: {int(m.iloc[0].N)} händelser, {int(m.iloc[0].G)} översyner. En hel översyn
utelämnas i taget. Modellerna använder samma förhandskarakteristika och antingen
inget mängdmått, förhandsvärderat kvartalsnetto, eller en kvadratrotsproxy skalad
med volatilitet och normal handelsvolym. RMSE i procentenheter:
'''
    for x in m.itertuples():text+=f'  {x.model}: {x.leave_review_out_RMSE:.3f}\n'
    text+=f'''Punktskattningarna visar ingen förbättring av att lägga till dessa köp-proxies.
Alla tre jämförelseintervall omfattar noll; materiella förbättringar ryms också.
Det är inte ett strukturellt test av enskilda order: kvartalsnetto är endogent,
tidpunkten saknas och modellerna skiljer både normalisering och funktionsform.
Beslut: ingen påvisad extra information om priserna från just dessa proxies.
Detta utesluter inte att faktiska indexorder påverkar priset.
Källa: models/REPORT.txt, formal_model_comparisons.csv, VALIDATION.json.

3. SYNLIGA BLANKNINGSPOSITIONER — GENOMFÖRT MED NYA FI-EXPORTER
{sh['issuer_event_count']} tilläggshändelser, {sh['companies']} bolag, {sh['reviews']} översyner,
{sh['pair_count']} innehavare×händelser i den frysta offentliga baslinjekohorten.
Aktuell och historisk FI-export hämtades tillsammans. Den gamla historikfilen
ensam saknade vissa aktuella slutpositioner. Båda äldre datagrindar bevaras.
Måttet är icke-negativ nettokortexponering; en undertrösklig eller nettolång
position är inte en observerad nolla. Konservativa intervall används.
Lika översynsviktat intervall för förändring före genomförandet:
[{b['build_lower_pp']:.3f}; {b['build_upper_pp']:.3f}] procentenheter emitterat kapital.
Efterförändring: [{b['after_change_lower_pp']:.3f}; {b['after_change_upper_pp']:.3f}].
Tillfällig topp säkert positiv i {sh['issuer_hump_status']['certain_positive']} av
{sh['issuer_event_count']} händelser, strikt positiv topp utesluten i
{sh['issuer_hump_status']['strict_positive_impossible']}, oavgjord i
{sh['issuer_hump_status']['undetermined']}.
Detta är identifieringsintervall från censurerade rapporter, INTE 95%-intervall.
Beslut: en smal positionsbeskrivning, ingen marknadsomfattande motpartsanalys.
Långt innehav som köps före och säljs vid bytet kräver ingen nettokortposition;
testet kan därför inte utesluta arbitrage eller fastställa prisorsaken.
Källa: short_positions/REPORT.txt, RESULTS.json och verifieringsfiler.

4. ANDRA VINNARSTRUKTURER OCH OUTNYTTJAD DATA — GENOMFÖRBARHET
Ny förkvartalskontroll visar {int(n.issuer_distinct_stock_candidates.min())}–{int(n.issuer_distinct_stock_candidates.max())}
emittentdistinkta kandidater, {int(n.funds_with_positions.min())}–{int(n.funds_with_positions.max())} fonder och
{int(n.managers_with_positions.min())}–{int(n.managers_with_positions.max())} fondbolag per översyn.
Men {100*(n.pairs_shared_fund/n.pair_count).min():.1f}–{100*(n.pairs_shared_fund/n.pair_count).max():.1f}% av aktieparen delar redan någon fond.
En enkel gemensam-ägare-indikator är nästan mättad. Viktade benchmarknätverk
kan ge en separat riskfråga, men varken nyhetsurvalet eller tidigare svensk
samvariationsforskning försvinner. INGA nätverksavkastningar har räknats.
Kassa/derivat: relevanta XML-fält finns, men exponerings- och flödeskedjan är
inte komplett. Vanlig omviktning av oförändrade medlemmar: historiska indexvikter,
float och indexaktier saknas; ett nytt kausalt prisexperiment är inte klart.
Beslut: behåll som dokumenterade datagränser/idéer, inte genomförda resultat.
Källa: frontier/decision_register.txt och network_feasibility.json.

TOLKNING OCH LEVERANS
De tidigare selektivt lästa vinnarna visar flera möjliga strukturer; de visar
inte vad som orsakar ett prisbeslut. Att en mekanism förblir öppen gör inte alla
resultat värdelösa, men dessa nya körningar ger inget stöd för att lova ett pris.
Fler ospecificerade regressionsvarianter gör inte kausaliteten säkrare.

Alla nya ekonomiska utfallsanalyser är explorativa efter omfattande tidigare
analys. Deklarationer före respektive körning är inte blind preregistrering.
Kod: code/build/omxsb_broadening_20261102. Data och beslut: motsvarande output/.
Original och felrättelser är bevarade. Inga FTN-utfall, ingen uppsatstext.
Ändringarna är lokala; inga commits eller pushar gjordes i denna runda.
'''
    (O/'RESULTAT.txt').write_text(text)
    (U/'OMXSB_breddad_provning_20261102.txt').write_text(text)
    readme='''REPLAY / SAVED ANALYSIS
Use the project's Python environment with pandas, numpy, scipy, statsmodels.
Run from repository root. These depend on existing project data and frozen inputs;
they are not fresh downloads or a new blind pre-analysis plan.

python code/build/omxsb_broadening_20261102/switchers/run.py --repo . --out output/omxsb_broadening_20261102/switchers
python code/build/omxsb_broadening_20261102/switchers/validate.py --out output/omxsb_broadening_20261102/switchers
python code/build/omxsb_broadening_20261102/models/compare.py --repo . --out output/omxsb_broadening_20261102/models
python code/build/omxsb_broadening_20261102/models/verify.py --repo . --out output/omxsb_broadening_20261102/models
python code/build/omxsb_broadening_20261102/frontier/network_feasibility.py --repo . --out output/omxsb_broadening_20261102/frontier

For short positions, use its module-specific replay instructions. Do not rebuild
the source or cohort gate over a frozen version. All earlier invalid attempts
are provenance only, not additional specifications to select from.
'''
    (O/'README.txt').write_text(readme)
    files=[p for d in [D,O] for p in d.rglob('*') if p.is_file() and p.name!='PACKAGE_SHA256.json' and '__pycache__' not in p.parts]
    hashes={str(p.relative_to(R)):digest(p) for p in sorted(files)}
    (O/'PACKAGE_SHA256.json').write_text(json.dumps(hashes,indent=2))
    z=U/'OMXSB_breddad_provning_20261102.zip'
    with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED) as zz:
        for p in files+[O/'PACKAGE_SHA256.json']:zz.write(p,p.relative_to(R))
    with zipfile.ZipFile(z) as zz:assert zz.testzip() is None
    print(json.dumps({'output_files':len(hashes),'zip_bytes':z.stat().st_size,'zip':str(z),'report':str(U/'OMXSB_breddad_provning_20261102.txt')},indent=2))

if __name__=='__main__':finish()
