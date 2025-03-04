resource "aws_lambda_function" "function" {
  count         = length(var.handler_method_mapping)
  function_name = "${var.resource_prefix}-${var.handler_method_mapping[count.index].name}"

  # filename         = data.archive_file.zipped_code[count.index].output_path
  # source_code_hash = data.archive_file.zipped_code[count.index].output_base64sha256
  filename         = var.handler_method_mapping[count.index].handler_file_path
  source_code_hash = filebase64sha256(var.handler_method_mapping[count.index].handler_file_path)

  handler = var.handler_method_mapping[count.index].handler_package

  memory_size                    = 256
  timeout                        = 30
  runtime                        = "python3.13"
  reserved_concurrent_executions = -1

  architectures = [var.lambda_arch]

  kms_key_arn = var.kms_key_arn

  role = var.lambda_execution_role

  environment {
    variables = var.environment_variables
  }
}

resource "aws_lambda_permission" "api_gateway" {
  count         = length(var.handler_method_mapping)
  statement_id  = "AllowExecutionFromApiGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.function[count.index].function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${data.aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
}

# data "archive_file" "zipped_code" {
#   count       = length(var.handler_method_mapping)
#   type        = "zip"
#   source_file = var.handler_method_mapping[count.index].handler_file_path
#   output_path = "${var.resource_prefix}-${var.handler_method_mapping[count.index].name}.zip"
# }
