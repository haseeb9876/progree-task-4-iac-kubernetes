"""Commands scoped explicitly to the local Task 4 cluster."""
from pathlib import Path
import json
import shutil
import subprocess
ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'progree-task4'
NAMESPACE = PROFILE
MINIKUBE = shutil.which('minikube') or 'C:/Program Files/Kubernetes/Minikube/minikube.exe'

def run(*args, **kwargs):
    return subprocess.run(list(args), check=True, text=True, encoding='utf-8', **kwargs)

def k(*args, capture=False, input=None):
    command = [MINIKUBE, '-p', PROFILE, 'kubectl', '--', '--context', PROFILE, *args]
    return run(*command, capture_output=capture, input=input).stdout

def read(*args):
    return json.loads(k(*args, '-o', 'json', capture=True))


def load_image(image):
    """Stream a host Docker archive directly into the node runtime."""
    import tempfile
    with tempfile.TemporaryDirectory(prefix='task4-image-') as tmp:
        archive = Path(tmp) / 'image.tar'
        run('docker', 'save', '-o', str(archive), image)
        # Binary stdin avoids Windows SCP and nested /tmp mount visibility.
        with archive.open('rb') as source:
            subprocess.run(['docker', 'exec', '-i', PROFILE, 'ctr', '--namespace',
                            'k8s.io', 'images', 'import', '--local',
                            '--platform', 'linux/amd64', '-'], stdin=source, check=True)
