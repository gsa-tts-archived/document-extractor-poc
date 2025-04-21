resource "aws_iam_role" "execution_role" {
  name = "${local.project}-${var.environment}-lambda-execution-role"

  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy" "lambda_basic_execution" {
  name = "AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "attach_basic_permission_to_role" {
  role       = aws_iam_role.execution_role.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

data "aws_iam_policy_document" "dynamodb_lambda_policy" {
  statement {
    effect    = "Allow"
    actions   = ["dynamodb:*"]
    resources = [aws_dynamodb_table.extract_table.arn]
  }
}

resource "aws_iam_policy" "dynamodb_lambda_policy" {
  name   = "${local.project}-${var.environment}-dynamodb-lambda-policy"
  policy = data.aws_iam_policy_document.dynamodb_lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "attach_dynamodb_permission_to_role" {
  role       = aws_iam_role.execution_role.name
  policy_arn = aws_iam_policy.dynamodb_lambda_policy.arn
}

data "aws_iam_policy_document" "s3_lambda_policy" {
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.document_storage.arn,
      "${aws_s3_bucket.document_storage.arn}/*",
    ]
  }
}

resource "aws_iam_policy" "s3_lambda_policy" {
  name   = "${local.project}-${var.environment}-s3-lambda-policy"
  policy = data.aws_iam_policy_document.s3_lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "attach_s3_permission_to_role" {
  role       = aws_iam_role.execution_role.name
  policy_arn = aws_iam_policy.s3_lambda_policy.arn
}

data "aws_iam_policy_document" "kms_lambda_policy" {
  statement {
    effect = "Allow"
    actions = [
      "kms:DescribeKey",
      "kms:Decrypt",
      "kms:Encrypt",
      "kms:GenerateDataKey",
    ]
    resources = [aws_kms_key.encryption.arn]
  }
}

resource "aws_iam_policy" "kms_lambda_policy" {
  name   = "${local.project}-${var.environment}-kms-lambda-policy"
  policy = data.aws_iam_policy_document.kms_lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "attach_kms_permission_to_role" {
  role       = aws_iam_role.execution_role.name
  policy_arn = aws_iam_policy.kms_lambda_policy.arn
}

data "aws_iam_policy_document" "sqs_lambda_policy" {
  statement {
    effect    = "Allow"
    actions   = ["sqs:*"]
    resources = [aws_sqs_queue.queue_to_dynamo.arn]
  }
}

resource "aws_iam_policy" "sqs_lambda_policy" {
  name   = "${local.project}-${var.environment}-sqs-lambda-policy"
  policy = data.aws_iam_policy_document.sqs_lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "attach_sqs_permission_to_role" {
  role       = aws_iam_role.execution_role.name
  policy_arn = aws_iam_policy.sqs_lambda_policy.arn
}

data "aws_iam_policy_document" "secrets_lambda_policy" {
  statement {
    effect    = "Allow"
    actions   = ["secretsmanager:*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "secrets_lambda_policy" {
  name   = "${local.project}-${var.environment}-secrets-lambda-policy"
  policy = data.aws_iam_policy_document.secrets_lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "attach_secrets_permission_to_role" {
  role       = aws_iam_role.execution_role.name
  policy_arn = aws_iam_policy.secrets_lambda_policy.arn
}

data "aws_iam_policy" "lambda_textract_execution" {
  name = "AmazonTextractFullAccess"
}

resource "aws_iam_role_policy_attachment" "attach_textract_permission_to_role" {
  role       = aws_iam_role.execution_role.name
  policy_arn = data.aws_iam_policy.lambda_textract_execution.arn
}
