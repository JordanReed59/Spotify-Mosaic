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

########## Lambda configuration ##########
data "archive_file" "python_code_zip" {
type        = "zip"
source_dir  = "${path.module}/../../src/backend"
output_path = "${path.module}/python/mosaify.zip"
}

resource "aws_lambda_function" "terraform_lambda_func" {
filename                       = "${path.module}/python/mosaify.zip"
function_name                  = "mosaify_backend"
role                           = aws_iam_role.lambda_role.arn
handler                        = "test.lambda_handler"
runtime                        = "python3.8"
depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
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