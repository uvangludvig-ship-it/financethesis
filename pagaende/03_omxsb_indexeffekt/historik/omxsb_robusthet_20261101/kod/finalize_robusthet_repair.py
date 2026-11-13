"""Package the already computed repair and record provenance; no return calculations."""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import zipfile

REPO=Path(__file__).resolve().parents[2]
OUT=REPO/'output/omxsb_robusthet_20261101'


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def replace_block(path,start,end,text):
    original=path.read_text()
    if start in original:
        before,tail=original.split(start,1)
        _,after=tail.split(end,1)
        updated=before+start+'\n'+text+'\n'+end+after
    else:
        updated=original.rstrip()+'\n\n'+start+'\n'+text+'\n'+end+'\n'
    path.write_text(updated)


def main():
    validation=json.loads((OUT/'validation.json').read_text())
    if validation.get('status')!='passed':raise RuntimeError('Validate the corrected outputs before packaging.')
    (OUT/'requirements.lock').write_text(''.join(f'{p}=={importlib.metadata.version(p)}\n' for p in ['numpy','pandas','scipy','pyarrow','statsmodels']))
    (OUT/'KORNING.md').write_text('''# Körning och vad som valideras

Rättelse efter kända resultat, version5. Inga FTN-utfall eller rådata ändras.

Kör från repot med Python och beroendena i requirements.lock. I denna granskning användes /tmp/omxsb-audit-venv/bin/python.

1. python code/build/test_robusthet_repair.py
2. python code/claude_checks/test_twin_first_stage.py
3. python code/claude_checks/twin_first_stage.py --repo . --output-dir output/omxsb_robusthet_20261101/first_stage_validation
4. python code/build/robusthet_hela.py
5. python code/build/validate_robusthet_repair.py
6. python code/build/finalize_robusthet_repair.py

Steg3 skriver metadata/NA och returnerar avsiktligt exitkod2 när förstastegets underlag är ofullständigt. Det är inte ett ekonomiskt nollresultat och ska inte döljas som lyckad skattning. Fortsätt med den oberoende kontrollanalysen i steg4. Kör inte hela listan med ett villkor som kräver exit0 från valideringsspärren.

Rootens robusthet_hela.py är kompatibilitetsstart; notebooken anropar samma kanoniska analyskod. Den sista paketeringen lägger även till valideringsresultat, testkod och dokumentation i robusthet_hela_resultat.zip.

Valideringen jämför samtliga T2-medel och intervall med statsmodels, kontrollerar matcher, tidsgränser och NA-status, och bekräftar att450 gemensamma event-CAR är oförändrade mot den föregående exporten. Tio inferens-/urvalstester och fyra förstastegstester passerar. Det verifierar implementationen, inte en kausal design.

Original i archive/robusthet_repair_20261101/. Gamla robusthet_hela_resultat/ är markerad SUPERSEDED. Aktuella tabeller ligger i denna mapp. Primärtabellen results.csv innehåller explicita spärrade T5-rader; tolka inte saknade skattningar som0.
''')
    archive=REPO/'archive/robusthet_repair_20261101'
    frozen=json.loads((archive/'original_sha256.json').read_text())
    for relative,digest in frozen.items():
        if sha(archive/relative)!=digest:raise RuntimeError('Archived original changed: '+relative)
    all_archived={str(p.relative_to(archive)):sha(p) for p in sorted(archive.rglob('*')) if p.is_file() and p.name not in ['original_sha256.json','all_archived_sha256.json']}
    (archive/'all_archived_sha256.json').write_text(json.dumps(all_archived,indent=2)+'\n')
    sources=['code/build/robusthet_hela.py','code/build/test_robusthet_repair.py',
             'code/build/validate_robusthet_repair.py','code/build/finalize_robusthet_repair.py',
             'code/claude_checks/twin_first_stage.py','code/claude_checks/test_twin_first_stage.py',
             'code/notebooks/robusthet_hela_panelen.ipynb','robusthet_hela.py','robusthet_hela_panelen.ipynb',
             'thesis/design/ROBUSTHET_RATTELSE_20261101.md','thesis/design/OMXSB_TOLKNINGSREGLER.md',
             'thesis/design/OMXSB_struktur.md']
    artifacts={str(p.relative_to(REPO)):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='artifact_manifest.json'}
    artifacts.update({p:sha(REPO/p) for p in sources})
    (OUT/'artifact_manifest.json').write_text(json.dumps(artifacts,indent=2)+'\n')
    rows=['## OMXSB control-analysis repair, 1 November 2026','',
          'Post-result code/method repair. Original exports archived, raw sources unchanged. Source hashes in output/omxsb_robusthet_20261101/input_sha256.json; artifact hashes in artifact_manifest.json. No FTN return calculations.','',
          '| File | Provenance/status |','|---|---|']
    for p in sorted(OUT.rglob('*')):
        if p.is_file():rows.append(f'| `{p.relative_to(REPO)}` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |')
    rows.append('| `robusthet_hela_resultat.zip` | Current code, specification, results, provenance and tests; supersedes archived original ZIP. |')
    replace_block(REPO/'data/MANIFEST.md','<!-- OMXSB_ROBUSTHET_REPAIR_20261101 -->','<!-- END_OMXSB_ROBUSTHET_REPAIR_20261101 -->','\n'.join(rows))
    log='| 1 Nov 2026 | Codex with independent code/document reviews | Repair OMXSB control-analysis code and unsupported interpretations at user request | Fixed review weighting, nonoverlapping covariates, outcome-blind control selection, future-event filtering and export schemas; reran T2 on full available panel; T5 flagged unestimable with unresolved membership; historical first-stage false zeros replaced by explicit validation/NA status; corrected design notes, preserved originals, added14 tests and independent saved-output checks; no FTN returns | No; technical code, audit and planning notes only |'
    replace_block(REPO/'thesis/AI_LOG.md','<!-- OMXSB_ROBUSTHET_REPAIR_20261101 -->','<!-- END_OMXSB_ROBUSTHET_REPAIR_20261101 -->','\n'.join(['| Date | Tool | Purpose | What changed | Thesis text? |','|---|---|---|---|---|',log]))
    with zipfile.ZipFile(REPO/'robusthet_hela_resultat.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob('*')):
            if p.is_file():z.write(p,'results/'+str(p.relative_to(OUT)))
        for relative in sources:z.write(REPO/relative,relative)
    print(json.dumps({'zip':str(REPO/'robusthet_hela_resultat.zip'),'sha256':sha(REPO/'robusthet_hela_resultat.zip'),'artifacts':len(artifacts)},ensure_ascii=False))


if __name__=='__main__':main()
