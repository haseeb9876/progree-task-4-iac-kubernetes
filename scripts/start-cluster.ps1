$ErrorActionPreference = 'Stop'
$minikubeCommand = Get-Command minikube -ErrorAction SilentlyContinue
$minikubeExe = if ($minikubeCommand) { $minikubeCommand.Source } else { 'C:/Program Files/Kubernetes/Minikube/minikube.exe' }
if (-not (Test-Path -LiteralPath $minikubeExe)) { throw 'Install Minikube first: winget install --id Kubernetes.minikube --exact' }
& $minikubeExe start -p progree-task4 --driver=docker --cpus=2 --memory=4096 --addons=metrics-server --keep-context
if ($LASTEXITCODE -ne 0) { throw 'Cluster startup failed' }
& $minikubeExe addons enable traefik -p progree-task4
if ($LASTEXITCODE -ne 0) { throw 'Ingress setup failed' }
& $minikubeExe -p progree-task4 kubectl -- get nodes
if ($LASTEXITCODE -ne 0) { throw 'Cluster verification failed' }
