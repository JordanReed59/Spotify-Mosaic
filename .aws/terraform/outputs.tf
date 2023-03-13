output "website_url" {
  value = aws_s3_bucket_website_configuration.website_bucket.website_endpoint
}

# output "api_base_url" {
#   value = "${aws_api_gateway_deployment.deploy_api.invoke_url}/img"
# }