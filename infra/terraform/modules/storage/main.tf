variable "name_prefix" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

resource "aws_s3_bucket" "lotes" {
  bucket_prefix = "${var.name_prefix}-lotes-"
  tags          = merge(var.tags, { Name = "${var.name_prefix}-lotes" })
}

resource "aws_s3_bucket_public_access_block" "lotes" {
  bucket                  = aws_s3_bucket.lotes.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lotes" {
  bucket = aws_s3_bucket.lotes.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "lotes" {
  bucket = aws_s3_bucket.lotes.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.lotes.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.lotes.arn
}
