mock_provider "aws" {}

run "isolated_network_layout" {
  command = plan
  assert {
    condition     = length(aws_subnet.private) == 2 && length(aws_subnet.public) == 2
    error_message = "The network must span two public and two private subnets."
  }
  assert {
    condition     = alltrue([for s in aws_subnet.private : !s.map_public_ip_on_launch])
    error_message = "Private subnets must not assign public addresses."
  }
  assert {
    condition     = length(distinct(concat(aws_subnet.private[*].cidr_block, aws_subnet.public[*].cidr_block))) == 4
    error_message = "Subnet ranges must be distinct."
  }
  assert {
    condition     = aws_subnet.private[0].availability_zone != aws_subnet.private[1].availability_zone
    error_message = "Private subnets must span availability zones."
  }
  assert {
    condition     = aws_route.internet.destination_cidr_block == "0.0.0.0/0"
    error_message = "The public route table needs an internet route."
  }
}
run "reject_duplicate_zones" {
  command = plan
  variables { availability_zones = ["us-east-1a", "us-east-1a"] }
  expect_failures = [var.availability_zones]
}
