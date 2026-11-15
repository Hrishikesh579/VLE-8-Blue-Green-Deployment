output "instance_id" {
  description = "Existing EC2 instance ID"
  value       = data.aws_instance.vle8_host.id
}

output "public_ip" {
  description = "Public IP of the existing EC2 instance"
  value       = data.aws_instance.vle8_host.public_ip
}

output "private_ip" {
  description = "Private IP of the existing EC2 instance"
  value       = data.aws_instance.vle8_host.private_ip
}

output "instance_type" {
  description = "Existing EC2 instance type"
  value       = data.aws_instance.vle8_host.instance_type
}