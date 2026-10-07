# Task 4 evidence

All execution records in this directory describe this laptop's local Minikube
profile `progree-task4`, except Terraform's explicitly mocked provider tests.
They are not GitHub-hosted CI or live cloud deployment results.

| Evidence | What it proves |
| --- | --- |
| [Cluster setup](cluster-setup.json) | Ready node, storage class, metrics API, Traefik |
| [Runtime checks](runtime-checks.txt) | Ingress, health, validation, authentication API, CRUD, cache invalidation |
| [Runtime record](runtime.json) | Test time and successful application verification |
| [Persistence and recovery](resilience.json) | Same PVC and data after MongoDB pod replacement; backend pod recovery |
| [HPA samples](hpa.json) | Actual load-phase expansion and cooldown to two replicas |
| [Workload snapshot](workloads.json) | Ready pod state and exact deployed image identities |
| [Terraform checks](terraform-tests.txt) | Two successful provider-mock tests |
| [Terraform scope](terraform.json) | Validation passed; no cloud resources created |

Reproduce with the commands in the main README. `scripts/verify-all.py` saves
UTF-8 logs and stops on failures; `scripts/capture-runtime.py` records a compact
healthy snapshot without secrets. The report builder refuses to generate a
success report unless all required local evidence records report success.

Cloud VPC creation, EKS/GKE provisioning, node failure tolerance, database
replication, and a highly available control plane are not verified here. See
[architecture limits](../ARCHITECTURE.md). No application credentials or kubeconfig
are included in this evidence.
