# Task 4 implementation checklist

Source: Progree DevOps Tasks & Instructions PDF, Task 4.
Selected execution environment: local Minikube, as requested.

| Requirement | Implementation target | Evidence required |
| --- | --- | --- |
| Isolated networks declared with IaC | Terraform cloud network configuration; provider still to be selected | Formatting/validation plus real plan/apply only when cloud use is authorized |
| Containerized application on Kubernetes | Standalone Wanderlust frontend/backend, MongoDB, Redis | Ready pods and passing API checks |
| Persistent volume claims | MongoDB StatefulSet with PVC | Record survives pod replacement |
| Ingress endpoint | Traefik routing to frontend/backend services | Actual browser/API request through Ingress |
| HPA | CPU requests, metrics-server, autoscaling/v2 HPA | Measured replicas increase under load and settle after load stops |
| Availability | Multiple stateless replicas, probes, disruption budgets | Recovery after deleting an application pod |
| Highly available cluster | Architecture documented separately from laptop demo | Single laptop cannot verify control-plane or node failure tolerance |

## Delivery stages

1. Install and verify Minikube prerequisites; record cluster evidence.
2. Add standalone application sources with attribution and Kubernetes manifests.
3. Deploy, run persistence/recovery/Ingress/HPA checks, record real outcomes.
4. Add declarative infrastructure appropriate to the selected cloud provider.
5. Produce the final PDF and presentation instructions from recorded evidence.

The setup repository is not a claim that all Task 4 requirements are complete.
Tasks 2 and 3 remain independent projects with separate data and ports.
