provider "aws" {
  region = var.aws_region
}

# Centralizar o arquivo de controle de estado do terraform
terraform {
  backend "s3" {
    bucket = "terraform-state-igti-${numero_conta}"
    key    = "state/igti/edc/mod1/terraform.tfstate"
    region = aws_region
  }
}
