"""Validate and publish this collection into new paths; refuses every overwrite."""
import collections, csv, datetime as dt, hashlib, json, pathlib, re, shutil, sys, zipfile
import xml.etree.ElementTree as ET
from decimal import Decimal

ROOT=pathlib.Path(__file__).resolve().parents[2]
RAW=ROOT/'data/raw/ap';META=RAW/'_collection_20261031';FI=ROOT/'data/raw/fi_short'
stage=pathlib.Path(sys.argv[1]);out=ROOT/'data/derived/ap'
now=dt.datetime.now(dt.timezone.utc).isoformat()

def read_csv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write_csv(p,rows,fields):
    with p.open('x',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def write_text(p,s):
    with p.open('x',encoding='utf-8') as f:f.write(s)

rows=read_csv(stage/'ap_svenska_aktier_med_ric.csv')
checks=read_csv(stage/'source_checks.csv')
assert not read_csv(stage/'parse_rejections.csv')
assert len(rows)==len(read_csv(stage/'ap_svenska_aktier_2013_2026.csv'))
assert all(r['datum'].endswith(('06-30','12-31')) and '2013'<=r['datum'][:4]<='2026' for r in rows)
assert all(Decimal(r['antal_aktier'])>=0 and Decimal(r['marknadsvarde'])>=0 for r in rows)
assert all(Decimal(r['antal_aktier'])==int(Decimal(r['antal_aktier'])) for r in rows)
assert all(not r['ISIN'] or re.fullmatch(r'[A-Z]{2}[A-Z0-9]{9}[0-9]',r['ISIN']) for r in rows)
keys=[(r['fond'],r['datum'],r['ISIN']) for r in rows if r['ISIN']]
assert len(keys)==len(set(keys)), 'Duplicate source ISIN within fund/date'
assert all(not r['RIC'] or r['RIC'] in r['RIC_kandidater'].split('|') for r in rows)
assert all(not r['RIC'] for r in rows if r['samlat_aktieslag']=='true')
assert all(not r['RIC'] for r in rows if r['matchningsmetod'].startswith('fuzzy'))

# Sum-of-rounded-items tolerance, based on the displayed source unit/precision.
controls=[]
for c in checks:
    if not c['source_total_sek']:continue
    date=c['datum']
    quantum=1 if date in ('2020-12-31','2021-06-30') else (1000000 if date>='2021-12-31' else (100000 if date<='2017-06-30' and date!='2016-12-31' else 10000))
    tolerance=Decimal(int(c['rows'])+1)*Decimal(quantum)/2
    difference=abs(Decimal(c['difference_sek']))
    assert difference<=tolerance,(c,tolerance)
    controls.append(dict(fond=c['fond'],datum=date,source_total_sek=c['source_total_sek'],extracted_total_sek=c['extracted_total_sek'],difference_sek=c['difference_sek'],rounding_tolerance_sek=str(tolerance),status='PASS'))

# Verify original bytes against download hashes.
requests=[json.loads(x) for x in (META/'requests.jsonl').read_text().splitlines()]
for rec in requests:
    if rec.get('status')==200 and rec.get('local_path'):
        assert hashlib.sha256((ROOT/rec['local_path']).read_bytes()).hexdigest()==rec['sha256']

# FI's ODS mixes real date cells (older rows) and ISO text (newer rows).
fi_file=FI/'HistoriskaPositioner_2026-10-31.ods'
with zipfile.ZipFile(fi_file) as z:
    assert z.read('mimetype')==b'application/vnd.oasis.opendocument.spreadsheet'
    tree=ET.fromstring(z.read('content.xml'))
ns={'t':'urn:oasis:names:tc:opendocument:xmlns:table:1.0'}
fi_dates=[]
for row in tree.findall('.//t:table-row',ns):
    cells=row.findall('t:table-cell',ns)
    if len(cells)<5:continue
    vals=[' '.join(c.itertext()).strip() for c in cells]
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}',vals[4]):fi_dates.append(vals[4])
    elif cells[4].get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}date-value'):
        fi_dates.append(cells[4].get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}date-value')[:10])
assert len(fi_dates)>30000

bydate=collections.Counter((r['fond'],r['datum']) for r in rows)
pages={'AP1':'https://www.ap4.se/om-ap4/om-ap1/','AP2':'https://ap2.se/forvaltning/innehav/','AP3':'https://www.ap3.se/forvaltning/ap3s-portfolj/ap3s-vardepapper','AP4':'https://www.ap4.se/rapporter/innehavslistor/'}
coverage=[]
for fund in pages:
    for year in range(2013,2027):
        for md in ('06-30','12-31'):
            date=f'{year}-{md}'; count=bydate[fund,date]
            sources=sorted({r['kallurl'] for r in rows if r['fond']==fund and r['datum']==date})
            status='downloaded_parsed' if count else 'missing_on_current_official_site'
            reason='' if count else 'Ingen fullständig innehavslista funnen i aktuellt officiellt arkiv eller kompletterande sökning; detta bevisar inte att listan aldrig publicerats.'
            if fund=='AP1' and year==2026:
                status='not_applicable_fund_closed';reason='AP1 upphörde vid utgången av 2025. Tillgångarna överfördes till AP3/AP4 från 2026-01-01.'
            elif date>'2026-10-31':
                status='future_reporting_date';reason='Rapportdatumet ligger efter insamlingsdagen 2026-10-31.'
            elif fund=='AP2' and date=='2017-12-31':
                status='missing_wrong_date_link';reason='2017-avsnittet länkar till en fil som uttryckligen är daterad 2018-03-31. Den filen har sparats men inte ersatt 2017-12-31.'
            coverage.append(dict(fond=fund,datum=date,status=status,svenska_aktier_rader=count,url='|'.join(sources),arkiv_url=pages[fund],kontrollerad_utc=now,kommentar=reason))
assert len(coverage)==112 and len(bydate)==66

out.mkdir(parents=True,exist_ok=False)
for f in stage.glob('*.csv'):
    with (out/f.name).open('xb') as dest:dest.write(f.read_bytes())
write_csv(META/'coverage.csv',coverage,list(coverage[0]))
missing=[r for r in coverage if r['status']!='downloaded_parsed']
write_csv(META/'missing_lists.csv',missing,list(coverage[0]))
write_csv(META/'source_total_validation.csv',controls,list(controls[0]))
log_fields=['url','source_page','downloaded_at_utc','kind','method','status','final_url','content_type','local_path','bytes','sha256','error']
write_csv(RAW/'download_log_2026-10-31.csv',requests,log_fields)
fi_requests=[r for r in requests if 'fi.se' in r['url']]
write_csv(FI/'download_log_2026-10-31.csv',fi_requests,log_fields)

classification=[
    {'ISIN':'LU1778762911','bolag':'Spotify','url':'https://investors.spotify.com/stock-info/default.aspx','grund':'XNYS: SPOT; notering i New York, inte på svensk börs.'},
    {'ISIN':'US7311054099','bolag':'Polestar ADS','url':'https://polestar.gcs-web.com/ir-resources/investor-faqs','grund':'PSNY, Nasdaq New York. AP4 anger också källticker PSNY US.'},
    {'ISIN':'CA76131D1033','bolag':'Restaurant Brands International','url':'https://www.rbi.com/investors/faqs/','grund':'QSR på New York Stock Exchange och Toronto Stock Exchange sedan december 2014.'},
    {'ISIN':'US2575592033','bolag':'Domtar','url':'https://www.sec.gov/Archives/edgar/data/1381531/000156459016013475/ufs-10k_20151231.htm','grund':'Emittentens Form 10-K: UFS, New York/Toronto; AP2:s rad anger US TRADED.'},
]
for c in classification:c['kontrollerad_utc']=now
write_csv(META/'classification_sources.csv',classification,list(classification[0]))

inputs=[]
for rel in ['data/input/omxsb/omxsb_events_with_ric_2007_2026.csv','data/raw/lseg/panel_2012_2026/stocks_static.csv','data/raw/lseg/panel_2005_2026/stocks_static_2005.csv']:
    p=ROOT/rel;inputs.append(dict(path=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
summary=dict(created_at_utc=now,holdings_rows=len(rows),fund_rows=dict(collections.Counter(r['fond'] for r in rows)),fund_dates=len(bydate),coverage_status=dict(collections.Counter(r['status'] for r in coverage)),ric_populated=sum(bool(r['RIC']) for r in rows),ric_unambiguous_identifier_matches=sum(r['osaker_matchning']=='false' for r in rows),ric_uncertain_or_unmatched=sum(r['osaker_matchning']=='true' for r in rows),parse_rejections=0,duplicate_fund_date_isin=0,source_totals_checked=len(controls),source_total_checks_passed=True,fi_data_rows=len(fi_dates),fi_min_position_date=min(fi_dates),fi_max_position_date=max(fi_dates),input_hashes=inputs)
write_text(META/'validation_summary.json',json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
for src in ('/tmp/ap4_2026_p3.png',):
    with (META/pathlib.Path(src).name).open('xb') as f:f.write(pathlib.Path(src).read_bytes())

write_text(RAW/'INSAMLINGSLOGG_2026-10-31.md',f'''# AP- och FI-insamling 2026-10-31

Insamlingen är delvis komplett: {len(bydate)} av 112 efterfrågade fond/datum-kombinationer har innehavsdata. CSV-filen innehåller {len(rows):,} rader. Inga datum har fyllts ut med närliggande observationer och frånvaro av en lista betyder inte noll innehav.

| Fond | Hämtade halvår | Saknade publicerade perioder |
|---|---:|---|
| AP1 | 2: 2025-06-30, 2025-12-31 | Båda halvåren 2013–2024 |
| AP2 | 22: 2015-06-30–2026-06-30, utom 2017-12-31 | Båda halvåren 2013–2014 samt 2017-12-31 |
| AP3 | 19: 2017-06-30–2026-06-30 | Båda halvåren 2013–2016 |
| AP4 | 23: 2015-06-30–2026-06-30 | Båda halvåren 2013–2014 |

AP1:s verksamhet upphörde 2025-12-31 enligt [AP4:s AP1-arkiv]({pages['AP1']}); 2026 markeras därför som ej tillämpligt. För AP2–AP4 är 2026-12-31 ett framtida rapportdatum, inte en redan förfallen publicering. Totalt: 40 äldre listor ej funna, 1 felaktigt daterad arkivlänk, 2 ej tillämpliga fond/datum och 3 framtida datum.

## Filer och spårbarhet

- `AP1/`–`AP4/`: oförändrade PDF-original, inklusive utländska aktielistor när fonden publicerar dem separat. 110 innehavsfiler sparades, varav 107 avser efterfrågade halvår. Tre extra filer från AP2 (2018-03-31 svenska/utländska samt 2024-04-04 utländska) ligger kvar som dokumentation av arkivets länkar och används inte i CSV-filen. AP4:s årsredovisning 2014 sparades också för kontroll; den innehåller endast största innehaven och används inte som ersättning för en fullständig lista.
- `download_log_2026-10-31.csv`: samtliga HTTP-hämtningar/försök och FI:s lyckade webbläsarhämtning, med URL, nedladdningstid i UTC, lokal sökväg, storlek, SHA-256 och eventuellt fel.
- `_collection_20261031/requests.jsonl`: löpande maskinläsbar logg. HTML-sidor och dokumentlänkar sparas bredvid den.
- `_collection_20261031/coverage.csv`: exakt en rad för var och en av de 112 efterfrågade kombinationerna. `missing_lists.csv` innehåller de 46 som inte har data.
- `../../derived/ap/ap_svenska_aktier_2013_2026.csv`: de sex efterfrågade kolumnerna. **Marknadsvärde anges i SEK**, omräknat från källans kr/TSEK/MSEK. Antal aktier är källans antal, utan splitjustering. Decimaltecken är punkt; CSV-avgränsare är komma; UTF-8 med BOM.
- `../../derived/ap/ap_svenska_aktier_med_ric.csv`: samma rader med RIC, osäkerhetsflaggor, käll-URL, PDF-sida och rad, källenhet och klassificeringsgrund.
- `../../derived/ap/matchningar_att_granska.csv`: alla osäkra eller omatchade rader, inklusive eventuella RIC-förslag.
- `../../derived/ap/excluded_rows.csv`: bortvalda utländska innehav, rättigheter, privata kreditfonder/skuldebrev och bolagssummor som annars skulle dubbelräknas med aktieslagsrader. Tomma ISIN har aldrig ersatts med ett påhittat värde.

## Definition och begränsningar

”Svenska aktier” tolkas som svenska aktiemarknaden, inklusive utländska emittenter noterade i Sverige. Urvalet utgår från fondernas svenska aktielistor/Sverige-avsnitt. Identifierade avvikelser (Spotify, Polestar ADS, Domtar och Restaurant Brands) har lyfts bort; de redovisas med primärkällor i `classification_sources.csv`. Det är inte en oberoende historisk noteringsdatabas: källornas kvarvarande nollvärdesinnehav behålls och flaggas för granskning av noteringsstatus.

AP1 har inga marknadskoder: svenska ISIN används, kompletterat med utländska ISIN som samma datum förekommer i övriga fonders svenska listor. Dessa utländska AP1-rader flaggas särskilt; samma ISIN kan handlas på flera marknader och AP1:s exakta handelsplats kan inte avgöras ur filen.

AP2 anger på många listor att innehaven är **netto efter utlånade aktier**. Därför är AP2:s antal inte utan vidare jämförbara med bruttoägande hos andra fonder. Källvärden har inte justerats för värdepappersutlåning.

AP4 redovisar ibland aktieslag samlat (särskilt 2019-12-31 och 2023-12-31). Sådana rader behålls, med `samlat_aktieslag=true` och tom RIC. Sammanskrivna ISIN bevaras i `kall_ISIN` men inte som ett falskt enskilt ISIN i huvudkolumnen. När källan visar både bolagssumma och aktieslag används endast aktieslagen.

## RIC-matchning

Eventkälla: `data/input/omxsb/omxsb_events_with_ric_2007_2026.csv`. Exakt ISIN prioriteras. Där eventlistan saknar ISIN används de befintliga LSEG-filerna `panel_2012_2026/stocks_static.csv` och `panel_2005_2026/stocks_static_2005.csv`, endast för RIC som faktiskt finns i eventlistan.

Namn normaliseras för versaler, diakritik, skiljetecken och bolagssuffix; aktieslag bevaras. En entydig exakt normaliserad namnmatch kan få RIC men är **alltid flaggad som osäker**. Bolagsmatch utan säkert aktieslag, identifierarkonflikt och ungefärlig namnmatch ger endast kandidater, ingen automatisk RIC. RIC för flera aktieslag fördelas aldrig på en samlad innehavsrad. Eventlistan är inte ett fullständigt börsregister; många stora permanenta indexmedlemmar saknar därför match.

{summary['ric_populated']:,} rader har ifylld RIC, varav {summary['ric_unambiguous_identifier_matches']:,} har entydig identifierarmatch. Övriga {summary['ric_uncertain_or_unmatched']:,} rader är flaggade för osäker match eller saknad eventmatch. `osaker_matchning=false` avser identitetsmatchen, inte en oberoende kontroll av historisk handelsplats eller noteringsstatus.

## Kontroller

Alla sparade original har verifierats mot nedladdningshash. Datum läses ur PDF-innehållet. Noll felaktigt tolkade kandidatrader återstår, inga dubbletter av fond/datum/ISIN finns och inga negativa antal eller marknadsvärden förekommer. AP4:s 23 svenska delsummeringar stämmer inom den högsta möjliga effekten av källans avrundning. AP4 2026-06-30 har grafiska rubriker och summa som saknas i textlagret; summan 144 755 MSEK och avgränsningen till sidorna 1–3 har kontrollerats visuellt. Kontrollbilden sparas i `_collection_20261031/ap4_2026_p3.png`. Representativa sidor för AP1, AP2, AP3 samt äldre och nyare AP4 har också granskats visuellt.

`source_checks.csv` visar summering före instrument-/marknadsurval, för jämförelse med originalets svenska avsnitt (för AP1 samtliga lästa aktier). Där källan saknar totalsumma lämnas kontrollen tom. Full kontrollsammanställning finns i `_collection_20261031/validation_summary.json` och `source_total_validation.csv`.

## FI

Original: `../fi_short/HistoriskaPositioner_2026-10-31.ods`. FI:s nuvarande exportformat är ODS, trots att sidan kallar filerna Excelfiler. Den sparade filen är en verifierad ODS med {len(fi_dates):,} positionsrader och positionsdatum {min(fi_dates)}–{max(fi_dates)}. Äldre datum är datumceller medan nyare ofta är textceller; originalformatet har bevarats.

Direkta HTTP-försök mot exportadressen gav 404. Hämtning via knappen ”Historiska positioner” på [FI:s register](https://www.fi.se/sv/vara-register/blankningsregistret/) i Chrome lyckades; den filen har kopierats byte för byte till repot. Filen avser offentliga betydande korta nettopositioner, inte samtliga rapporterade småpositioner; `<0,5` är en rapporterad tröskelpassage och inte nödvändigtvis noll.

## Sökta luckor och reproduktion

AP1:s aktuella domän och tidigare innehavssida leder nu till AP4:s information med listor för 2025. Den äldre officiella CDN-domänen kunde inte DNS-upplösas. AP2:s offentliga dokumentindex för 2013 och 2014 innehöll rapporter men inga innehavslistor. AP3:s aktuella innehavsarkiv börjar 2017. AP4:s årssökning 2014 gav inga innehavslistor; årsredovisningen hänvisar till en separat fullständig lista men visar själv endast fem största. Kompletterande webbsökningar efter respektive fonds äldre listor gav inga ytterligare fullständiga original på fondernas nuvarande webbplatser. Saknade perioder har inte ersatts med sammanfattningar eller tredjepartsrekonstruktioner.

Insamlingen har endast skrivit nya filer under `data/raw/ap`, `data/raw/fi_short`, `data/derived/ap` och nya fristående skript i `code/build`. Befintliga källfiler har enbart lästs. Andra pågående arbeten i det gemensamma repot har inte ändrats eller återställts.

Extraktionen kan upprepas utan nätverk med `python3 code/build/parse_ap_20261031.py --out /tmp/ny_tom_katalog` (Poppler/pdftotext krävs). Alla utdata skrivs exklusivt; välj en sökväg som inte redan finns. Hämtaren och slutkontrollen har tidsstämplade namn i `code/build`. FI-hämtningen kräver webbplatsens knapp om den direkta exportadressen fortsatt ger 404.
''')
write_text(FI/'README_2026-10-31.md',f'''# FI Historiska positioner

Originalfil: `HistoriskaPositioner_2026-10-31.ods` (oförändrad ODS).
Hämtad 2026-10-31 via Historiska positioner på https://www.fi.se/sv/vara-register/blankningsregistret/.
Exportadress: https://www.fi.se/BlankningsRegister/GetHistFile . Direkta anrop gav 404; Chrome-knappen fungerade.
{len(fi_dates):,} datarader, positionsdatum {min(fi_dates)}–{max(fi_dates)}. Filen innehåller offentliga betydande korta nettopositioner, inte alla positioner ned till anmälningsgränsen. `<0,5` ska inte behandlas som noll.
URL, UTC-tid och SHA-256 finns i `download_log_2026-10-31.csv`. Full insamlingslogg finns i `../ap/INSAMLINGSLOGG_2026-10-31.md`.
''')
print(json.dumps(summary,ensure_ascii=False,indent=2))
