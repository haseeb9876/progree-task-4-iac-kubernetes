# Task 4: Infrastructure as Code and Kubernetes

Progree DevOps Internship ? Haseeb Ullah.

This is the separate Task 4 project. The selected environment is local Minikube
on Windows 10 with Docker Desktop. No paid cloud resources are authorized.

## Assignment requirements

- Declarative Terraform or CloudFormation for isolated cloud networks.
- Deploy the containerized application to Kubernetes.
- Persistent volume claims, Ingress endpoints, and Horizontal Pod Autoscalers.
- An elastic, highly available architecture.

## Local cluster setup

Start Docker Desktop with Linux containers. Install Minikube:

```powershell
winget install --id Kubernetes.minikube --exact
```

Open a new PowerShell window after installation. Run from this repository:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/start-cluster.ps1
minikube -p progree-task4 kubectl -- get nodes
minikube -p progree-task4 kubectl -- get pods -A
minikube -p progree-task4 kubectl -- top nodes
py -3 scripts/verify-cluster.py
```

The script creates the dedicated `progree-task4` profile with 2 CPUs and 4096 MiB,
metrics-server for autoscaling metrics, and Traefik for Ingress. It preserves the
previous default kubectl context; always specify this profile or context.
The execution-policy option applies only to this script process.

The Minikube-matched kubectl avoids client/server version mismatch with Docker's
bundled kubectl. Default hostpath storage supports local PVC demonstrations.

```powershell
# Preserve cluster and application data when stopping:
minikube stop -p progree-task4
# Restart:
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/start-cluster.ps1
```

On Windows with the Docker driver, the node IP is not directly browser-accessible.
Use a localhost port-forward to the Ingress controller for the application demo.
Do not delete the profile or PVCs unless you intend to remove their data.

## Completion boundary

Cluster setup is the first stage. Application manifests, PVC persistence tests,
Ingress request tests, HPA load tests, declarative network infrastructure, and the
final proof PDF must be completed and evidenced before calling Task 4 complete.
A single-node local cluster cannot prove node-level high availability. Multiple
application replicas can demonstrate pod recovery, but all share one laptop.
Cloud networking will remain unverified until a separately authorized cloud run.

## References

- [Minikube Docker driver](https://minikube.sigs.k8s.io/docs/drivers/docker/)
- [Traefik addon](https://minikube.sigs.k8s.io/docs/handbook/addons/traefik/)
- [Original Task 2](https://github.com/haseeb9876/progree-task-2-containerization)
- [Original Task 3](https://github.com/haseeb9876/progree-task-3-cicd)
