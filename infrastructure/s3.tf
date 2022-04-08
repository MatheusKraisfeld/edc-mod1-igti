resource "aws_s3_bucket" "dl" {
  bucket = "datalake-kraisfeld-igti-edc-tf"

  tags = {
    IES   = "IGTI",
    CURSO = "EDC"
  }
}

resource "aws_s3_bucket_acl" "dl" {
  bucket = aws_s3_bucket.dl.id
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "dl" {
  bucket = aws_s3_bucket.dl.id

  rule {
    apply_server_side_encryption_by_default {
      # kms_master_key_id = data.aws_kms_key.s3.arn
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket" "stream" {
  bucket = "igti-kraisfeld-streaming-bucket"
  acl    = "private"

  tags = {
    IES   = "IGTI",
    CURSO = "EDC"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}