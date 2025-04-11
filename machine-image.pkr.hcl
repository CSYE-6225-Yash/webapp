packer {
  required_plugins {
    amazon = {
      version = ">= 1.0.0, < 2.0.0"
      source  = "github.com/hashicorp/amazon"
    }
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = "~> 1"
    }
  }
}

# Adding source for creating machine image on aws
source "amazon-ebs" "webapp-aws-ami" {
  ami_name        = "webapp-${formatdate("YYYY-MM-DD-hh-mm-ss", timestamp())}"
  ami_description = "AMI for webapp"
  instance_type   = "${var.instance_type}"
  region          = "${var.aws_region}"
  source_ami      = "${var.source_ami}"
  ssh_username    = "${var.ssh_username}"
  ami_users       = ["${var.dev_account}", "${var.demo_account}"]

  aws_polling {
    delay_seconds = 60
    max_attempts  = 50
  }

  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/sda1"
    volume_type           = var.volume_type
    volume_size           = var.volume_size
  }
}

# Adding source for creating machine image on gcp
source "googlecompute" "webapp-gcp-mi" {
  image_name        = "webapp-${formatdate("YYYY-MM-DD-hh-mm-ss", timestamp())}"
  image_description = "Machine image for webapp"
  project_id        = "${var.project_id}"
  source_image      = "${var.source_image}"
  ssh_username      = "${var.ssh_username}"
  zone              = "${var.zone}"
  disk_size         = var.disk_size
  machine_type      = var.machine_type
}

# Building image
build {
  # Building custom image for aws and gcp simultaneously
  sources = [
    "source.amazon-ebs.webapp-aws-ami",
    # "source.googlecompute.webapp-gcp-mi"
  ]

  # Sending webapp.zip to instance for building machine image
  provisioner "file" {
    source      = "webapp.zip"
    destination = "/tmp/webapp.zip"
  }

  # Sending cloud-agent-config.json to instance for configuration of cloud watch agent
  provisioner "file" {
    source      = "cloudwatch-agent-config.json"
    destination = "/tmp/cloudwatch-agent-config.json"
  }

  # Updating server
  provisioner "shell" {
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive"
    ]
    script = "update_server.sh"
  }

  # Setting up webapp
  provisioner "shell" {
    environment_vars = [
      "user=${var.user}"
    ]
    script = "webapp_setup.sh"
  }

  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}