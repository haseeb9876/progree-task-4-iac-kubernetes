"""Capture a compact, non-secret runtime snapshot for the report."""
import datetime
import json
from cluster import ROOT, NAMESPACE, read
pods=[p for p in read('-n',NAMESPACE,'get','pods')['items'] if not p['metadata'].get('deletionTimestamp')]
assert pods and all(any(c['type']=='Ready' and c['status']=='True' for c in p['status'].get('conditions',[])) for p in pods)
record={'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pods':[{'name':p['metadata']['name'],'node':p['spec']['nodeName'],'ready':True,'images':[{'name':c['name'],'image':c['image'],'imageID':c['imageID']} for c in p['status']['containerStatuses']]} for p in pods], 'pvc':[{'name':v['metadata']['name'],'status':v['status']['phase'],'volume':v['spec']['volumeName']} for v in read('-n',NAMESPACE,'get','pvc')['items']], 'ingress':[{'name':i['metadata']['name'],'class':i['spec']['ingressClassName']} for i in read('-n',NAMESPACE,'get','ingress')['items']]}
(ROOT/'docs/evidence/workloads.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('Captured healthy pods, image identities, PVC and Ingress without secrets.')
