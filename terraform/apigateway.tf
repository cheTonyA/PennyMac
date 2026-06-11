resource "aws_api_gateway_rest_api" "stocks_api" {
  name = "${var.project_name}-${var.environment}-api"
}

resource "aws_api_gateway_resource" "movers" {
  rest_api_id = aws_api_gateway_rest_api.stocks_api.id
  parent_id   = aws_api_gateway_rest_api.stocks_api.root_resource_id
  path_part   = "movers"
}

resource "aws_api_gateway_method" "get_movers" {
  rest_api_id   = aws_api_gateway_rest_api.stocks_api.id
  resource_id   = aws_api_gateway_resource.movers.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.stocks_api.id
  resource_id = aws_api_gateway_resource.movers.id
  http_method = aws_api_gateway_method.get_movers.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api_lambda.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_lambda.function_name
  principal     = "apigateway.amazonaws.com"
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda
  ]

  rest_api_id = aws_api_gateway_rest_api.stocks_api.id

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.stocks_api.id
  stage_name    = "dev"
}