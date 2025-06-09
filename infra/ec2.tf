module "security_group" {
  source = "terraform-aws-modules/security-group/aws"

  name        = var.product_name
  use_name_prefix = false
  description = "Security group for ${var.product_name} server"
  vpc_id      = data.aws_vpc.default_vpc.id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_ipv6_cidr_blocks = [ "::/0"]

  ingress_rules = ["http-80-tcp", "https-443-tcp"]

  egress_rules = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]

}

module "ec2_instance" {
  source = "terraform-aws-modules/ec2-instance/aws"

  name = "${var.product_name}"

  instance_type = var.instance_type
  ami = data.aws_ami.ubuntu.id
  ignore_ami_changes = true

  user_data_base64 = base64encode(file("${path.module}/files/user-data.sh"))

  availability_zone = element(local.azs, 0)
  vpc_security_group_ids = [module.security_group.security_group_id]

  create_iam_instance_profile = true
  iam_role_description        = "IAM role for EC2 instance"
  iam_role_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }
}
