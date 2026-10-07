"""Record actual local cluster readiness; never include kubeconfig or secrets."""
import datetime
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MINIKUBE = shutil.which('minikube') or 'C:/Program Files/Kubernetes/Minikube/minikube.exe'
PROFILE = 'progree-task4'

def k(*args):
    return subprocess.check_output([MINIKUBE, '-p', PROFILE, 'kubectl', '--', '--context', PROFILE, *args], text=True, encoding='utf-8')

def data(*args):
    return json.loads(k(*args, '-o', 'json'))

nodes = data('get', 'nodes')['items']
assert nodes and all(any(c['type'] == 'Ready' and c['status'] == 'True' for c in n['status']['conditions']) for n in nodes), 'Node not Ready'
storage = data('get', 'storageclass')['items']
assert any(s['metadata'].get('annotations', {}).get('storageclass.kubernetes.io/is-default-class') == 'true' for s in storage), 'Default storage class missing'
api = data('get', 'apiservice', 'v1beta1.metrics.k8s.io')
assert any(c['type'] == 'Available' and c['status'] == 'True' for c in api['status']['conditions']), 'Metrics API not available'
classes = data('get', 'ingressclass')['items']
assert any(c['metadata']['name'] == 'traefik' for c in classes), 'Traefik ingress class missing'
pods = data('get', 'pods', '-n', 'kube-system')['items']
for name in ('metrics-server', 'traefik'):
    matches = [p for p in pods if name in p['metadata']['name']]
    assert matches and all(any(c['type'] == 'Ready' and c['status'] == 'True' for c in p.get('status', {}).get('conditions', [])) for p in matches), name + ' not Ready'
metrics = k('top', 'nodes')
record = {
    'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'profile': PROFILE,
    'nodes': [{'name': n['metadata']['name'], 'version': n['status']['nodeInfo']['kubeletVersion'], 'ready': True} for n in nodes],
    'default_storage_class': [s['metadata']['name'] for s in storage if s['metadata'].get('annotations', {}).get('storageclass.kubernetes.io/is-default-class') == 'true'],
    'metrics_api_available': True,
    'traefik_ready': True,
    'node_metrics': metrics.strip(),
    'scope': 'Cluster prerequisites only; not application, HPA scaling, persistence, cloud, or high-availability proof.'
}
output = ROOT / 'docs/evidence/cluster-setup.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps(record, indent=2))
