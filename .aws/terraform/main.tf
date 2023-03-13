########## Locals ##########
locals {
  lambda_layer_zips = fileset(path.module, "python_layer.z*")
}

########## S3 configuration ##########
resource "aws_s3_bucket" "bucket" {
  bucket = "static-website-test-jr59"
  force_destroy = true
}

resource "aws_s3_bucket_website_configuration" "website_bucket" {
  bucket = aws_s3_bucket.bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_cors_configuration" "example" {
  bucket = aws_s3_bucket.bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["POST"]
    allowed_origins = ["*"]
    expose_headers  = []
  }
}

resource "aws_s3_bucket_policy" "allow_public_access" {
  bucket = aws_s3_bucket.bucket.id
  policy = data.aws_iam_policy_document.allow_public_access.json
}

data "aws_iam_policy_document" "allow_public_access" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject"
    ]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    resources = [
      aws_s3_bucket.bucket.arn,
      "${aws_s3_bucket.bucket.arn}/*",
    ]
  }
}

########## API Gateway configuration ##########
resource "aws_api_gateway_rest_api" "gateway" {
  name        = "mosaify_api"
  description = "Terraform Serverless API Gateway for Mosaify"
}

resource "aws_api_gateway_resource" "get_method_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.gateway.id}"
  parent_id   = "${aws_api_gateway_rest_api.gateway.root_resource_id}"
  path_part   = "mosaify"
}

resource "aws_api_gateway_method" "get_method" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.get_method_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = "${aws_api_gateway_rest_api.gateway.id}"
  resource_id = "${aws_api_gateway_method.get_method.resource_id}"
  http_method = "${aws_api_gateway_method.get_method.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.mosaify_backend.invoke_arn}"
}

resource "aws_api_gateway_deployment" "deploy_api" {
  depends_on = [
    "aws_api_gateway_integration.lambda"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.gateway.id}"
  stage_name  = "test"
}

########## Lambda configuration ##########
data "archive_file" "python_code_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../src/backend"
  output_path = "${path.module}/python/mosaify.zip"
}

# issues: not able to update layer when I make changes to it
resource "aws_lambda_layer_version" "lambda_layer" {
  for_each            = local.lambda_layer_zips
  filename            = each.value
  layer_name          = "python_dependencies"
  compatible_runtimes = ["python3.8"]
  source_code_hash    = "${filebase64sha256(each.value)}"
}
# resource "aws_lambda_layer_version" "lambda_layer_1" {
#   filename            = "python_layer.zip"
#   layer_name          = "python_dependencies"
#   compatible_runtimes = ["python3.8"]
#   source_code_hash    = "${filebase64sha256("python_layer.zip")}"
# }
# resource "aws_lambda_layer_version" "lambda_layer_2" {
#   filename            = "python_layer.z01"
#   layer_name          = "python_dependencies"
#   compatible_runtimes = ["python3.8"]
#   source_code_hash    = "${filebase64sha256("python_layer.z01")}"
# }
# resource "aws_lambda_layer_version" "lambda_layer_3" {
#   filename            = "python_layer.z02"
#   layer_name          = "python_dependencies"
#   compatible_runtimes = ["python3.8"]
#   source_code_hash    = "${filebase64sha256("python_layer.z02")}"
# }
# resource "aws_lambda_layer_version" "lambda_layer_3" {
#   filename            = "python_layer.z02"
#   layer_name          = "python_dependencies"
#   compatible_runtimes = ["python3.8"]
#   source_code_hash    = "${filebase64sha256("python_layer.z02")}"
# }
resource "aws_lambda_function" "mosaify_backend" {
  filename                       = "${path.module}/python/mosaify.zip"
  function_name                  = "mosaify_backend"
  role                           = aws_iam_role.lambda_role.arn
  handler                        = "test.lambda_handler"
  runtime                        = "python3.8"
  source_code_hash               = "${data.archive_file.python_code_zip.output_base64sha256}" #allows for the src code to be updated
  # layers                         = [aws_lambda_layer_version.lambda_layer_1.arn, aws_lambda_layer_version.lambda_layer_2.arn, aws_lambda_layer_version.lambda_layer_3.arn]
  layers                         = [for layer in aws_lambda_layer_version.lambda_layer : layer.arn]
  depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}

resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowMosaifyAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.mosaify_backend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.gateway.execution_arn}/*/*"
}

########## Role configuration ##########
resource "aws_iam_role" "lambda_role" {
  name   = "mosaify-lambda-backend-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_role.json 
}

data "aws_iam_policy_document" "lambda_role" {
  statement {
    sid     = ""
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role        = aws_iam_role.lambda_role.name
  policy_arn  = aws_iam_policy.iam_policy_for_lambda.arn
}

resource "aws_iam_policy" "iam_policy_for_lambda" {
  name         = "mosaify-lambda-backend-role-policy"
  description  = "AWS IAM Policy for managing mosaify lambda role"
  policy       = data.aws_iam_policy_document.role_policy.json
}


data "aws_iam_policy_document" "role_policy" {
  statement {
    sid       = ""
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }
}