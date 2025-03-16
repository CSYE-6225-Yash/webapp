variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "source_ami" {
  type    = string
  default = "source_ami"
}

variable "ssh_username" {
  type    = string
  default = "ubuntu"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "dev_account" {
  type    = string
  default = ""
}

variable "demo_account" {
  type    = string
  default = ""
}

variable "volume_size" {
  type    = number
  default = 0
}

variable "volume_type" {
  type    = string
  default = ""
}

variable "user" {
  type    = string
  default = ""
}

# Variables for gcp

variable "project_id" {
  type    = string
  default = "development"
}

variable "source_image" {
  type    = string
  default = "source_img"
}

variable "zone" {
  type    = string
  default = "us-east1-b"
}

variable "disk_size" {
  type    = number
  default = 0
}

variable "machine_type" {
  type    = string
  default = ""
}