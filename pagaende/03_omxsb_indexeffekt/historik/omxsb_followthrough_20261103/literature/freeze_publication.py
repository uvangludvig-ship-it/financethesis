from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
files=['README.txt','REPORT_SV.txt','CLOSEST_PAPERS.csv','SOURCE_LEDGER.json','AUDIT_SCOPE.json','READ_LOG.json','build_audit.py','freeze_publication.py','PUBLICATION_ALLOWLIST.json','PUBLICATION_SHA256.json']
(p/'PUBLICATION_ALLOWLIST.json').write_text(json.dumps(files,indent=2)+'\n')
h={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in files if n!='PUBLICATION_SHA256.json'}
(p/'PUBLICATION_SHA256.json').write_text(json.dumps(h,indent=2)+'\n')
print(json.dumps({'allowlisted':len(files),'hashed':len(h),'manifest_sha256':hashlib.sha256((p/'PUBLICATION_SHA256.json').read_bytes()).hexdigest()}))
