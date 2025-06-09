resource "aws_iam_policy" "github_actions" {
  name = "github-actions-ssm"
  policy = data.aws_iam_policy_document.github_actions_ssm.json
}

module "iam_github_actions" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-user"

  name          = "github-actions-ssm"
  force_destroy = true

  policy_arns = [
    aws_iam_policy.github_actions.arn
  ]
}