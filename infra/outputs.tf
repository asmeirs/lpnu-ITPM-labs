output "instance_public_ip" {
  value = module.ec2_instance.public_ip
}

output "iam_access_key_id" {
  description = "The github user access key ID"
  value       = module.iam_github_actions.iam_access_key_id
}

output "iam_access_key_secret" {
  description = "The github user access key secret"
  value       = module.iam_github_actions.iam_access_key_secret
  sensitive   = true
}