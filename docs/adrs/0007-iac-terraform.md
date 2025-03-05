# 7. Terraform IaC (Infrastructure as Code) for Deploys

Date: 2025-03-05

## Status

Accepted.

## Context

Infrastructure as Code (IaC) is an industry best practice to get repeatable and resilient deployments of applications
and associated infrastructure into the cloud.

There are many IaC options to deploy to AWS.

- [Terraform](https://www.terraform.io).
- [Pulumi](https://www.pulumi.com).
- [CDK](https://aws.amazon.com/cdk/).
- [Ansible](https://www.ansible.com).
- [Chef](https://www.chef.io).
- [Puppet](https://www.puppet.com).

There are probably even more.

Terraform is multi-cloud, has a full-featured DSL, tracks state and dependencies, and is agentless.

## Decision

Terraform will be used to deploy our infrastructure into the cloud.

## Consequences

We'll have a well supported IaC ecosystem to pull from.  No negative consequences.
