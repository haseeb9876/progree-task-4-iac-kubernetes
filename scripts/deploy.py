"""Build and deploy only the standalone local Task 4 environment."""
import json
import sys
from cluster import ROOT, MINIKUBE, PROFILE, NAMESPACE, k, run, load_image
run(sys.executable, str(ROOT / 'scripts/setup-local.py'))
k('apply', '-f', str(ROOT / 'k8s/namespace.json'))
secret = {'apiVersion': 'v1', 'kind': 'Secret', 'metadata': {'name': 'runtime-secrets', 'namespace': NAMESPACE}, 'type': 'Opaque', 'stringData': {p.name: p.read_text().strip() for p in (ROOT / '.secrets').iterdir() if p.is_file()}}
# Credentials travel through stdin, not process arguments, logs, or tracked files.
k('apply', '-f', '-', input=json.dumps(secret))
for component in ('backend', 'frontend'):
    image = f'progree-task4-{component}:local'
    run('docker', 'build', '-t', image, '--build-arg', 'APP_REVISION=task4-local', str(ROOT / component))
    load_image(image)
for source in json.loads((ROOT / 'config/image-sources.json').read_text()).values():
    # Use the exact public upstream digest in the node runtime, without aliases.
    run('docker', 'exec', PROFILE, 'crictl', 'pull', source)
for name in ('config.json', 'data.json'):
    k('apply', '-f', str(ROOT / 'k8s' / name))
for resource in ('statefulset/mongodb', 'deployment/redis'):
    k('-n', NAMESPACE, 'rollout', 'status', resource, '--timeout=600s')
for name in ('application.json', 'routing-scaling.json'):
    k('apply', '-f', str(ROOT / 'k8s' / name))
for deployment in ('backend', 'frontend'):
    k('-n', NAMESPACE, 'rollout', 'restart', 'deployment/' + deployment)
for resource in ('statefulset/mongodb', 'deployment/redis', 'deployment/backend', 'deployment/frontend'):
    k('-n', NAMESPACE, 'rollout', 'status', resource, '--timeout=600s')
print('Task 4 deployed. Run scripts/serve.ps1, then scripts/verify-stack.py.')
