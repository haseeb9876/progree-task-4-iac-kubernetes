# Optional AWS network blueprint

This declarative network module is prepared for the PDF cloud-network requirement.
AWS is an example target only. The authorized deployment is local Minikube.
**No AWS resources have been provisioned.** Mock tests are not real cloud plans.

It defines a dedicated VPC, public/private subnets across two availability zones,
an internet gateway, and separate route tables. Private subnets have no internet
route, NAT gateway, or public-address assignment. This module does not create EKS.
Minikube runs locally and is not attached to this VPC.

Credential-free checks:

```powershell
terraform init -backend=false
terraform fmt -check
terraform validate
terraform test
```

A later cloud deployment requires account, region/AZ choices, budget, access,
egress or private endpoints, and an approved cluster/storage design. Never commit
credentials, state, saved plans, or private variable files. No apply is automated.
