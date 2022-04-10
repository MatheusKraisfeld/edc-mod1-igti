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

variable "key_pair_name" {
  default = "kraisfeld-ec2-airflow"
}

variable "airflow_subnet_id" {
  default = "subnet-016dde93f8c31d34e"
}

variable "vpc_id" {
  default = "vpc-07ad677cc4474d563"
}