terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.15.1"
    }
  }
}

# Configure the AWS Provider
# Using aws CLI to create the shared configuaration credentials file
# Location: C:\Users\%Username%\.aws
provider "aws" {
  shared_config_files      = ["C:\\Users\\thai\\.aws\\config"]
  shared_credentials_files = ["C:\\Users\\thai\\.aws\\credentials"]
}
