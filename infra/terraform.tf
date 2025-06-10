terraform {
  required_version = "= 1.5.2"
  backend "s3" {
    bucket = "infrastructure-state-447839932018"
    region = "eu-central-1"
    key    = "eu-central-1/infra-baseline/terraform.tfstate"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = local.tags
  }
}