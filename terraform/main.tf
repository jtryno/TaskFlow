terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "security-group" {
  name        = "taskflow-sg"
  description = "taskflow-sg created 2026-03-22T23:24:35.180Z"

  ingress {
    description = "SSH Connection"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Public access to the API"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "TaskFlow"
  }

}

resource "aws_instance" "taskflow-server" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.security-group.id]

  tags = {
    Name = "TaskFlow"
  }
}

resource "aws_eip" "taskflow-ec2-ip" {
  instance = aws_instance.taskflow-server.id

  tags = {
    Name = "TaskFlow"
  }
}
