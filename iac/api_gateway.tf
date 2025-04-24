resource "aws_api_gateway_rest_api" "api" {
  name        = "${local.project}-${var.environment}-api"
  description = "${local.project} API"
}

resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    redeployment_for_document    = module.document_endpoints.resource_method_integration_configuration_hash
    redeployment_for_document_id = module.document_id_endpoints.resource_method_integration_configuration_hash
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = "v1"
  deployment_id = aws_api_gateway_deployment.api_deployment.id
}

resource "aws_api_gateway_authorizer" "authorizer" {
  name                             = "${local.project}-${var.environment}-authorizer"
  rest_api_id                      = aws_api_gateway_rest_api.api.id
  authorizer_uri                   = aws_lambda_function.authorizer.invoke_arn
  authorizer_result_ttl_in_seconds = 300
}
