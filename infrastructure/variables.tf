variable "base_bucket_name" {
  default = "datalake-igti-tf"
}

variable "ambiente" {
  default = "producao"
}

variable "numero_conta" {
  default = "741358071637"
}

variable "aws_region" {
  default = "us-east-2"
}

variable "lambda_function_name" {
  default = "IGTIexecutaEMR"
}
