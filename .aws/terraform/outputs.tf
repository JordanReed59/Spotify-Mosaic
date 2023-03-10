output "website_url" {
  value = aws_s3_bucket_website_configuration.website_bucket.website_endpoint
}
