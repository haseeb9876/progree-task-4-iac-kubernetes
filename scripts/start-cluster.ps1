$ErrorActionPreference = 'Stop'
$minikubeCommand = Get-Command minikube -ErrorAction SilentlyContinue
$minikubeExe = if ($minikubeCommand) { $minikubeCommand.Source } else { 'C:/Program Files/Kubernetes/Minikube/minikube.exe' }
if (-not (Test-Path -LiteralPath $minikubeExe)) { throw 'Install Minikube first: winget install --id Kubernetes.minikube --exact' }
$baseDigest = 'gcr.io/k8s-minikube/kicbase@sha256:4a1c825b61479e6c898851ea66f13c620aaeab6002746e95067fc2c4b38a0b24'
docker pull $baseDigest
if ($LASTEXITCODE -ne 0) { throw 'Minikube base image pull failed' }
docker tag $baseDigest gcr.io/k8s-minikube/kicbase:v0.0.51
if ($LASTEXITCODE -ne 0) { throw 'Minikube base image tagging failed' }
& $minikubeExe start -p progree-task4 --driver=docker --cpus=2 --memory=4096 --addons=metrics-server --keep-context --kubernetes-version=v1.37.0 --base-image=gcr.io/k8s-minikube/kicbase:v0.0.51
if ($LASTEXITCODE -ne 0) { throw 'Cluster startup failed' }
& $minikubeExe addons enable traefik -p progree-task4
if ($LASTEXITCODE -ne 0) { throw 'Ingress setup failed' }
& $minikubeExe -p progree-task4 kubectl -- --context progree-task4 get nodes
if ($LASTEXITCODE -ne 0) { throw 'Cluster verification failed' }
