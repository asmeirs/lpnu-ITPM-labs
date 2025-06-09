locals {
  tags = {
    Terraform = true
    Product = var.product_name
  }

  azs = slice(data.aws_availability_zones.available.names, 0, 3)

  user_data = <<-EOT
    #!/bin/bash

    apt update && apt upgrade -y


    # Install AWS CLI

    echo "Istalling AWS-CLI..."
    apt install -y openjdk-17-jdk zip unzip
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    ./aws/install
    rm -f awscli2.zip


    # Install docker
    echo "Installing Docker..."
    apt update
    apt install -y ca-certificates curl git
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt update

    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    echo "Adding users to Docker group..."
    groupadd docker
    usermod -aG docker ubuntu

    # Clone repository with docker-compose and scripts
    TARGET_DIR=/home/ubuntu/calc-visualizer
    REPO_URL=https://github.com/asmeirs/lpnu-ITPM-labs.git
    BRANCH=main
    FOLDER=server

    mkdir -p $TARGET_DIR
    cd $TARGET_DIR
    git init
    git remote add origin $REPO_URL
    git config core.sparseCheckout true
    echo "$FOLDER" > .git/info/sparse-checkout
    git pull origin $BRANCH

    chown -R ubuntu:ubuntu $TARGET_DIR



  EOT
}