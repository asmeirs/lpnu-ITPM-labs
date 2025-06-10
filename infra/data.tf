data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {}

data "aws_vpc" "default_vpc" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name = "vpc-id"
    values = [data.aws_vpc.default_vpc.id]
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"]
}

data "aws_iam_policy_document" "github_actions_ssm" {
  statement {
    actions = [
      "ssm:StartSession",
      "ssm:SendCommand"
    ]
    effect    = "Allow"
    resources = [
      module.ec2_instance.arn,
      "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:document/SSM-SessionManagerRunShell",
      "arn:aws:ssm:${var.region}::document/AWS-RunShellScript"
    ]
  }
  statement {
    actions = ["ssm:ListCommandInvocations"]
    effect    = "Allow"
    resources = ["*"]
  }
  statement {
    actions   = ["ssmmessages:OpenDataChannel"]
    effect    = "Allow"
    resources = ["arn:aws:ssm:*:*:session/$${aws:userid}-*"]
  }
  statement {
    actions   = [
      "ssm:TerminateSession",
      "ssm:ResumeSession"
    ]
    effect    = "Allow"
    resources = ["arn:aws:ssm:*:*:session/$${aws:userid}-*"]
  }
}
