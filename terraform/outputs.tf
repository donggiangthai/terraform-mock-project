output "ec2_id" {
  value = aws_instance.terraform-instance.id
}

output "ec2_ami" {
  value = aws_instance.terraform-instance.ami
}
