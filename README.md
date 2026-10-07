# Task 4: Infrastructure as Code and Kubernetes

**Progree DevOps Internship - Haseeb Ullah**

Standalone Wanderlust deployment on a local Minikube cluster, with declarative
Kubernetes resources and an optional, undeployed Terraform cloud-network module.
Task 2 and Task 3 remain in their separate repositories.

## Start here

- [Task 4 proof PDF](docs/Task-4-IaC-Kubernetes-Report.pdf)
- [Architecture and limits](docs/ARCHITECTURE.md)
- [Presentation walkthrough](docs/PRESENTATION.md)
- [Assignment checklist](docs/TASK-4-PLAN.md)
- [Recorded evidence](docs/evidence/README.md)
- [Optional cloud-network blueprint](infra/aws-network/README.md)

## Windows prerequisites

Docker Desktop must be running with Linux containers and WSL2. The dedicated
`progree-task4` profile requests 2 CPUs and 4096 MiB. Keep other large workloads
stopped when running on a 16 GB laptop. Python 3 and Git are also required.

```powershell
winget install --id Kubernetes.minikube --exact
winget install --id Hashicorp.Terraform --exact
```

Open a new terminal after installing. Minikube 1.39.0 and Kubernetes 1.37.0 are
used by this setup. The script pulls a pinned base image and restores its tag
before starting, avoiding a Windows cache-import issue observed during setup.

## Start and deploy

Run these commands from this repository:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/start-cluster.ps1
py -3 scripts/verify-cluster.py
py -3 scripts/deploy.py
```

The execution-policy option applies only to that PowerShell process. Startup
preserves the previous default Kubernetes context. Scripts explicitly target
`progree-task4` and use Minikube's matched kubectl binary.

Deployment generates ignored credentials without replacing existing ones, builds
application images, imports them, pulls pinned database/cache images inside the node, applies
manifests, and waits for healthy workloads. Binary Docker archive streaming avoids
Windows SSH transfers and nested temporary-directory mount issues. Do not run two deployments simultaneously.

In another terminal, leave the following command running:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/serve.ps1
```

Open **http://localhost:8084**. Traffic passes through the Traefik Ingress service.
The Minikube node IP is not directly accessible from Windows with the Docker driver.

## Demonstrate and verify

```powershell
py -3 scripts/seed-demo.py
py -3 scripts/verify-all.py
py -3 scripts/capture-runtime.py
```

The resilience test intentionally replaces one database pod and one backend pod;
run it during a demonstration window, not while editing application data. It
retains the PVC and removes only its temporary test post. The HPA test generates
bounded HTTP traffic, removes its load job, and verifies return to two replicas.
Wait for the backend HPA to settle at two before running the load test.

```powershell
minikube -p progree-task4 kubectl -- --context progree-task4 -n progree-task4 get pods,pvc,ingress,hpa
minikube -p progree-task4 kubectl -- --context progree-task4 top nodes
```

## Terraform checks without cloud credentials

```powershell
terraform -chdir=infra/aws-network init -backend=false
terraform -chdir=infra/aws-network fmt -check
terraform -chdir=infra/aws-network validate
terraform -chdir=infra/aws-network test
```

Provider mocks check the declared network layout and reject duplicate availability
zones. They do not create infrastructure or validate real account permissions.
No Terraform apply or paid cloud deployment is authorized or automated.

## Regenerate the proof PDF

The committed PDF is built from the recorded successful local checks:

```powershell
py -3 -m venv .report-tools
.report-tools\Scripts\python.exe -m pip install reportlab
.report-tools\Scripts\python.exe scripts/build-report.py
```

The report covers the local Minikube deliverable and explicitly identifies the
remaining cloud deployment and full high-availability requirements.

## Stop without removing data

Stop the forwarding terminal with Ctrl+C, then:

```powershell
minikube stop -p progree-task4
```

Restart with the startup script and run the forwarding command again. Keep the
local `.secrets/` files together with the existing database data. Deleting the
profile or its PVCs can delete application data; ordinary stop preserves it.

## Scope and attribution

The local demo covers Kubernetes deployment, PVCs, Ingress and HPA verification.
The evidence folder records actual completed checks. A final report must only
claim checks that passed. Full cloud-network provisioning and highly available
node/control-plane/database operation are not demonstrated by this single laptop.

The application derives from the standalone Task 3 source and retains Wanderlust's
[MIT license](LICENSE). Read [architecture limits](docs/ARCHITECTURE.md) before
considering any public deployment; the inherited post API lacks authorization.

[Minikube Docker driver](https://minikube.sigs.k8s.io/docs/drivers/docker/) |
[Traefik addon](https://minikube.sigs.k8s.io/docs/handbook/addons/traefik/) |
[Kubernetes HPA](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/)
