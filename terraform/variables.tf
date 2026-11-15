variable "aws_region" {
  description = "AWS region containing the existing EC2 instance"
  type        = string
}

variable "existing_instance_id" {
  description = "ID of the existing VLE-7 EC2 instance reused by VLE-8"
  type        = string
}