terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.88.0"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      project = local.project
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "document-extractor-terraform-state"
    key            = ""
    region         = "us-east-1"
    dynamodb_table = "terraform_lock"
  }
}

locals {
  project = "document-extractor-${var.environment}"
}
