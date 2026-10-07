# Presenting Task 4

## Opening explanation

I used Minikube to run our application on Kubernetes. Declarative manifests
specify the desired replicas, persistent storage, routing, and autoscaling.
Kubernetes reconciles that desired state when pods fail or demand changes.
I also prepared and locally tested a Terraform cloud-network blueprint, but
have not deployed cloud resources.

## Technical demonstration

1. Show the separate repository and architecture diagram.
2. Show the Ready node and healthy pods using the Task 4 context.
3. Open http://localhost:8084 with the Ingress port-forward running.
4. Explain Ingress paths, ClusterIP services, and readiness probes.
5. Show MongoDB's bound PVC and the persistence verification record.
6. Show the pod replacement record and distinguish recovery from zero downtime.
7. Show HPA samples increasing under HTTP load and decreasing after load stops.
8. Explain the Terraform VPC/subnet/route configuration and mocked tests.
9. State that single-node Minikube and singleton databases are not fully HA.

## Questions to prepare for

**PVC versus pod?** A pod is replaceable compute; the claim references storage
whose lifecycle survives ordinary pod replacement.

**Service versus Ingress?** A Service gives pods a stable network endpoint;
Ingress uses HTTP routes to send browser requests to those services.

**HPA versus cluster autoscaling?** HPA changes pod replicas. Node autoscaling
changes machines and is not implemented by this local demo.

**What did Terraform actually deploy?** Nothing in a cloud account. The module
was validated and tested with a mock provider; cloud apply remains outstanding.

**Is this highly available?** It demonstrates replica recovery and elasticity.
A single laptop, single control-plane node and singleton database remain failure
points. The architecture document explains the changes needed for cloud HA.
