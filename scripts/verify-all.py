"""Run the local proof checks and preserve only actual successful outcomes."""
import datetime
import json
import subprocess
import sys
from cluster import ROOT
E = ROOT / 'docs/evidence'
E.mkdir(parents=True, exist_ok=True)
for script, log in [('verify-cluster.py','cluster-checks.txt'),('verify-stack.py','runtime-checks.txt'),('verify-resilience.py','resilience-checks.txt'),('verify-hpa.py','hpa-checks.txt')]:
    print('Running '+script,flush=True)
    result = subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,text=True,encoding='utf-8',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (E/log).write_text(result.stdout,encoding='utf-8')
    print(result.stdout,flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    if script=='verify-stack.py':
        assert 'All requested checks passed.' in result.stdout
        (E/'runtime.json').write_text(json.dumps({'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'passed','url':'http://127.0.0.1:8084','checks':'Frontend, SPA routes, readiness, validation, signup/signin, CRUD, cache invalidation, test cleanup'},indent=2)+'\n',encoding='utf-8')
print('All local Task 4 proof checks passed.',flush=True)
