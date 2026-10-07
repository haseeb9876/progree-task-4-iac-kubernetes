# Task 4 requirement checklist

Source: Progree DevOps Tasks & Instructions PDF, Task 4.
Selected execution environment: local Minikube, as requested.

| PDF requirement | Implementation | Verification |
| --- | --- | --- |
| Declarative cloud networks | Optional AWS Terraform VPC, four subnets across two zones, separate routes | Validate and provider-mock tests; no real cloud apply |
| Containerized stack on Kubernetes | Standalone frontend/backend, MongoDB, Redis | Ready pods and actual API checks |
| Persistent volume claims | MongoDB StatefulSet with 1 GiB PVC | Temporary post survives pod replacement with same PVC |
| Ingress endpoints | Traefik, localhost:8084 forwarding | Browser routes and API exercised through Ingress |
| HPA | Backend CPU requests and autoscaling/v2, 2 to 4 replicas | Ready replicas increase under real HTTP load and return to two |
| Elastic, highly available environment | Stateless replicas, probes, rolling updates, disruption budgets | Pod recovery and elasticity only; single-node/database failure tolerance is not provided |

[Recorded evidence](evidence/README.md) documents completed executions. The local
orchestration deliverable is separate from the remaining live cloud and full HA
objective. No cloud account, region or spending authorization was provided.
Tasks 2 and 3 remain independent projects with separate data and ports.
