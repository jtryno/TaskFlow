output "server_public_ip" {
  description = "The public IP address of the TaskFlow server"
  value       = aws_eip.taskflow-ec2-ip.public_ip
}

output "server_instance_id" {
  description = "The instance id"
  value       = aws_instance.taskflow-server.id
}

output "server_security_group_id" {
  description = "The ec2 security group id"
  value       = aws_security_group.security-group.id
}