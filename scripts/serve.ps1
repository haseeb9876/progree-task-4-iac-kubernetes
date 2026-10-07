$ErrorActionPreference = 'Stop'
$minikubeExe = 'C:/Program Files/Kubernetes/Minikube/minikube.exe'
& $minikubeExe -p progree-task4 kubectl -- --context progree-task4 -n kube-system port-forward service/traefik 8084:80 --address=127.0.0.1
if ($LASTEXITCODE -ne 0) { throw 'Task 4 Ingress port-forward stopped with an error' }
