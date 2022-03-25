# HCL - Hashicorp Configuration Language
# Linguaguem declarativa

resource "aws_s3_bucket" "datalake" {
  # Parâmetros de configuração do recurso escolhido
  bucket = "${var.base_bucket_name}-${var.ambiente}-${var.numero_conta}"

  tags = {
    IES   = "IGTI",
    CURSO = "EDC"
  }
}

resource "aws_s3_bucket_acl" "datalake" {
  bucket = aws_s3_bucket.datalake.id
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "datalake" {
  bucket = aws_s3_bucket.datalake.id

  rule {
    apply_server_side_encryption_by_default {
      # kms_master_key_id = data.aws_kms_key.s3.arn
      sse_algorithm = "AES256"
    }
  }
}
