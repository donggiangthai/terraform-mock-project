# Author information
variable "Author_name" {
  type        = string
  default     = "Dong Giang Thai"
  description = "The author name"
}
variable "Author_mail" {
  type        = string
  default     = "donggiangthai1998@gmail.com"
  description = "The author mail"
}

# AWS information
variable "AWS_REGION" {
  type        = string
  description = "AWS region"
}

variable "AWS_AMIS" {
  type        = map(string)
  description = "AWS AMI list"
}

variable "Base_NAME" {
  type        = string
  description = "Base tag Name"
}
