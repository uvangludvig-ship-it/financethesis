"""Package the executed OMXSB extension checks and register local provenance.

Analysis notes only; this does not write thesis prose, calculate FTN returns,
commit changes, or publish files. Run after the analysis and validation scripts.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--deliverables', type=Path, required=True)
    args = parser.parse_args()
    root = args.repo
    base = root / 'output/omxsb_extension_20261031'
    dest = args.deliverables
    dest.mkdir(parents=True, exist_ok=True)
    results = pd.read_csv(base / 'ownership/ownership_results.csv')
    summary = json.loads((base / 'ownership/run_summary.json').read_text())
    validation = json.loads((base / 'independent_validation.json').read_text())
    assert validation['status'] == 'passed'

    def cell(direction, group, sample='main_common'):
        z = results[results['sample'].eq(sample) & results.direction.eq(direction) & results.group.eq(group)]
        assert len(z) == 1
        return z.iloc[0]

    def number(v):
        return f'{v:+.3f}'.replace('.', ',')

    ap_lines = []
    for typ, label in [('addition', 'Inval'), ('deletion', 'Utträden')]:
        r = cell(typ, 'AP3_AP4_sum')
        ap_lines.append(f'{label}: AP3+AP4 {number(r.mean_pp)} procentenheter; 95%-intervall [{number(r.ci95_low)}; {number(r.ci95_high)}], {int(r.N)} observationer och {int(r.G)} översyner.')
    prior = cell('direction_aligned_pooled', 'AP3_AP4_sum', 'paired_event_minus_prior_182625day')
    txt = f'''UTFÖRT ARBETE OCH FAKTISKA RESULTAT – OMXSB, 31 OKTOBER 2026
Analysunderlag till författarna. Inte uppsatstext.

Arbetet har genomförts i samma lokala financethesis-repo. Det omfattar en ny AP-/FI-innehavsanalys, en avgränsad migrationsundersökning och en kandidatdatapilot. De tidigare avkastningsresultaten är bevarade. Inga FTN-avkastningar har beräknats. Ändringarna är lokala och inte pushade.

1. AP-/FI-ANALYSEN ÄR KÖRD
Frågan är om AP3 och AP4 ändrar sitt innehav i motsatt riktning runt OMXSB:s in- och utträden. Vi jämför samma aktier och samma halvårsdatum för AP-fonder och FI-fonder. Urvalet har {summary['main_common']} godkända indexändringar 2019–2025 från {summary['main_reviews']} översyner, av 230 ursprungliga kandidater. Nollor kräver en komplett innehavslista och tillräckligt säker identitet. Oklara aktieslag, enheter och bolagshändelser markeras eller utesluts med förklaring.

{chr(10).join(ap_lines)}

Måttet är förändrat antal aktier, justerat för verifierade splitar, dividerat med aktieslagets utestående antal vid slutdatum. Det är inte aktiens avkastning. Punktvärdena går åt motsatt håll mot indexändringen, men båda intervallen innehåller noll och även handel i samma riktning. Vi har alltså inte ett säkert belägg för att AP3/AP4 utgör en systematisk nettomotvikt.

Jämförelsen med samma aktiers föregående, eventfria halvår använder {int(prior.N)} indexändringar från {int(prior.G)} översyner. Efter justering för periodlängd är riktningsjusterad skillnad {number(prior.mean_pp)} procentenheter, intervall [{number(prior.ci95_low)}; {number(prior.ci95_high)}]. Positivt betyder samma riktning som indexändringen. Punkttecknet är alltså inte stabilt mellan huvudmåttet och denna bakgrundsjämförelse. Det är en beskrivande jämförelse, inte en kausal effekt.

Nordnet är en dokumenterad OMXSB-relaterad delgrupp. Nordea med historiskt rapporterat OMXSB-jämförelseindex redovisas separat, och den ursprungliga gruppen om 14 efterhandsklassificerade fonder används som känslighet. Ingen av dessa benämns hela marknadens indexkapital. AP2 redovisas separat eftersom dess listor är netto efter utlåning. 2026 ingår inte i huvudanalysen på grund av AP1:s portföljöverföringar.

Detta mäter rapporterade ägarförändringar över halvår, inte exakt när någon handlade eller vem motparten var. Svenska och utländska ägare utanför dessa register saknas. Kvarstående identifierings- och bolagshändelserisker framgår av detaljrapporten. Resultaten bevisar inte att det saknas säljare och förklarar inte i sig prisrörelserna.

2. MIGRATION HAR UNDERSÖKTS UTÖVER INDEXÖVERLAPP
Sex historiska Solactive-listor har jämförts över fem övergångsintervall mot 77 OMXSB-händelser. Två kandidater framkom: Addnode B december2023 och VBG B december2024. XACT Svenska Småbolags rapporterade innehav ökade från noll till 117686 respektive14915 aktier, samtidigt som den ursprungliga trackergruppen minskade sina innehav.

Exakt inträdesdag och fullständig mellanliggande ändringshistorik är inte slutverifierade. Därför kallas dessa kandidater, inte färdigverifierade migrationer. Två fall räcker inte för att mäta om migration dämpar priseffekten. Övriga undersökta aktier kan inte automatiskt klassas som utan migration, eftersom andra index inte är fullständigt kartlagda.

3. KANDIDATDATA FINNS FÖR TVÅ PILOTER; ANTICIPATIONSTESTET ÄR INTE FÄRDIGT
Nasdaqs originalfiler för oktober2019 och oktober2024 har hämtats. Samtliga29 berörda indexändringar matchar historiskt ticker och namn. Filerna innehåller historiska instrument, börsvärden, tolvmånadersomsättning och sektorer. De publicerades före respektive indexbesked men efter referensdagen.

Historisk free float, officiellt medlemskap, fullständiga identifierarlänkar och då gällande regelversioner återstår. Dagens statiska ISIN-koppling missar många historiska kontrollaktier. Därför har ingen prognosmodell eller ny förbeskedsavkastning beräknats med ett missvisande kontrollurval.

VAD DETTA BETYDER FÖR G&S
Den tidigare kompositionsanalysen är oförändrad. Migration är nu delvis kartlagd men inte fullt replikerad. Tidigare förbeskedsavkastning kvarstår som ett beskrivande mönster; den nya datapiloten löser inte identifieringen av förhandspositionering. Likviditets-/ägarspåret har fått en faktiskt körd utvidgning till AP3/AP4. Det är fortfarande fel att säga att alla fyra hypoteser nu är fullständigt prövade eller att G&S:s förklaring har bekräftats i Sverige.

KVALITET OCH REPRODUCERBARHET
Negativa FI-positioner skiljs från nollor; fond–värdepapper-par med oklar mängd utesluts symmetriskt. Aktieklasser och historiska namn kontrolleras, och utvalda felaktiga aktieantalsnämnare ersätts med emittentkällor. AP3/AP4:s publicerade listor har stämts av mot årsrapporter2019 och2024. Åtta missvisande etiketter i den tidigare resultatsammanställningen har korrigerats i en separat export, utan ändrade siffror.

De {validation['main_result_cells_independently_reestimated']} huvudcellerna har oberoende räknats om med statsmodels: medelvärden och intervall överensstämmer. Kandidat- och migrationskoden har körts igen från repot med samma data och gett samma beräknade resultat. Kontrollerna styrker beräkningarna och deras spårbarhet; de ersätter inte antaganden om datatäckning och identifiering.

Filer i leveransen: AP-detaljrapport, resultattabell, observationsjournal, exklusioner, migrationsrapport och kandidatpilot. Komplett kod och källunderlag finns lokalt i code/build/omxsb_*.py och output/omxsb_extension_20261031/ i financethesis-repot. Se KORNING.txt för körordning.
'''
    (base / 'UTFORT_OCH_RESULTAT.txt').write_text(txt)
    # Individual reports are copied separately after their filenames are frozen.
    for rel in ['UTFORT_OCH_RESULTAT.txt', 'KORNING.txt', 'independent_validation.json',
                'ownership/ANALYSRAPPORT.txt', 'ownership/KORNING.txt', 'ownership/RESULTAT_OVERSIKT.csv',
                'ownership/independent_rerun.json',
                'ownership/ownership_results.csv', 'ownership/ownership_observations.csv',
                'ownership/exclusion_journal.csv', 'migration/results/REPORT.txt',
                'candidate/PILOT_RESULTAT.txt', 'labels/label_changes.csv']:
        source = base / rel
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    # Capture full output inventory and hashes, without self-referential hash files.
    files = sorted(p for directory in [base, root / 'data/raw/omxsb_extension_20261031']
                   for p in directory.rglob('*') if p.is_file() and p.name != 'artifact_manifest.json')
    files += sorted(root / 'code/build' / name for name in [
        'omxsb_ap_prepare.py', 'omxsb_ap_ownership.py', 'omxsb_ap_validate.py', 'omxsb_candidate_pilot.py',
        'omxsb_migration_screen.py', 'omxsb_demand_labels.py', 'omxsb_relabel_results.py',
        'omxsb_extension_validate.py', 'omxsb_extension_finalize.py', 'audit_omxsb_results.py'])
    inventory = [{'path': str(p.relative_to(root)), 'bytes': p.stat().st_size,
                  'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    (base / 'artifact_manifest.json').write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + '\n')
    manifest = root / 'data/MANIFEST.md'
    marker = '<!-- OMXSB_EXTENSION_20261031 -->'
    end_marker = '<!-- END_OMXSB_EXTENSION_20261031 -->'
    existing = manifest.read_text()
    block = marker + '\n\n## OMXSB extension execution, 31 October 2026\n\n'
    block += 'Local analysis only. Original sources and earlier numerical exports preserved. No FTN returns. Full file hashes: `output/omxsb_extension_20261031/artifact_manifest.json`.\n\n'
    block += '| Location | Provenance / purpose |\n|---|---|\n'
    for path, purpose in [
        ('output/omxsb_extension_20261031/ownership/', 'New AP2/AP3/AP4 and FI half-year ownership analysis; source/exclusion ledgers and report; code/build/omxsb_ap_prepare.py and omxsb_ap_ownership.py'),
        ('output/omxsb_extension_20261031/candidate/', 'Nasdaq October2019/2024 original files and notices; two-review data pilot; source_manifest.json and source_reading_notes.json; code/build/omxsb_candidate_pilot.py'),
        ('output/omxsb_extension_20261031/migration/', 'Saved cached primary Solactive extracts plus original FI XML; bounded transition screen; source_register.csv; code/build/omxsb_migration_screen.py'),
        ('output/omxsb_extension_20261031/labels/', 'Eight corrected labels; original numerical results unchanged; code/build/omxsb_relabel_results.py'),
        ('data/raw/omxsb_extension_20261031/support/', 'Four official original PDFs and layout text extracts: government AP2019/2024, Nordnet2022, contemporaneous ENF2019 mandate statement; source_ledger.json'),
        ('output/omxsb_extension_20261031/independent_validation.json', 'Independent numerical/accounting checks; code/build/omxsb_extension_validate.py'),
    ]:
        block += f'| `{path}` | {purpose} |\n'
    block += '\n' + end_marker + '\n'
    if marker in existing:
        assert end_marker in existing, 'Incomplete previous extension manifest block'
        prefix, remainder = existing.split(marker, 1)
        _, suffix = remainder.split(end_marker, 1)
        updated = prefix + block + suffix
    else:
        updated = existing.rstrip() + '\n\n' + block
    manifest.write_text(updated)
    log = root / 'thesis/AI_LOG.md'
    log_text = log.read_text()
    line = '| 31 Oct 2026 | Codex with parallel agents | Execute missing OMXSB mechanism checks using existing results and newly collected data | New AP/FI half-year analysis, bounded cross-index migration screen, Nasdaq candidate-data pilot, label-only correction, source ledgers and independent numerical checks in output/omxsb_extension_20261031; local only, no FTN returns | No |'
    if line not in log_text:
        log.write_text(log_text.rstrip() + '\n' + line + '\n')
    print('Summary and deliverables:', dest)
    print('Registered source/output files:', len(inventory))


if __name__ == '__main__':
    main()
