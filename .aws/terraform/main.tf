resource "aws_s3_bucket" "bucket" {
  bucket = "static-website-test-jr59"
}

resource "aws_s3_bucket_website_configuration" "website_bucket" {
  bucket = aws_s3_bucket.bucket.id

  index_document {
    suffix = "index.html"
  }
}