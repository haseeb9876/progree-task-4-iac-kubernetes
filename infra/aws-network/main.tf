terraform {
  required_version = ">= 1.7.0, < 2.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = { Project = "progree-task4", ManagedBy = "Terraform" }
  }
}

variable "region" {
  type    = string
  default = "us-east-1"
}
variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
  validation {
    condition     = length(var.availability_zones) == 2 && length(distinct(var.availability_zones)) == 2
    error_message = "Provide two distinct availability zones in the chosen region."
  }
}
variable "vpc_cidr" {
  type    = string
  default = "10.44.0.0/16"
  validation {
    condition     = can(cidrsubnet(var.vpc_cidr, 8, 11))
    error_message = "The VPC CIDR must support the declared subnet layout."
  }
}

resource "aws_vpc" "cluster" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = { Name = "progree-task4" }
}
resource "aws_internet_gateway" "public" {
  vpc_id = aws_vpc.cluster.id
}
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.cluster.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = false
  tags                    = { Name = "task4-public-${count.index}", "kubernetes.io/role/elb" = "1" }
}
resource "aws_subnet" "private" {
  count                   = 2
  vpc_id                  = aws_vpc.cluster.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = false
  tags                    = { Name = "task4-private-${count.index}", "kubernetes.io/role/internal-elb" = "1" }
}
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.cluster.id
}
resource "aws_route" "internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.public.id
}
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
resource "aws_route_table" "private" {
  count  = 2
  vpc_id = aws_vpc.cluster.id
}
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}
# Deliberately no NAT, EKS, nodes, or load balancers in this network-only module.
# Private subnets have local VPC routes only. Cloud deployment needs an approved
# egress/endpoints and cluster plan; Minikube is not connected to this VPC.
output "vpc_id" { value = aws_vpc.cluster.id }
output "private_subnet_ids" { value = aws_subnet.private[*].id }
output "public_subnet_ids" { value = aws_subnet.public[*].id }
