output "dynamodb_table_name" {
  value = aws_dynamodb_table.stock_results.name
}

output "lambda_function_name" {
  value = aws_lambda_function.stock_processor.function_name
}

output "amplify_app_id" {
  value = aws_amplify_app.frontend.id
}

output "api_url" {
  value = "${aws_api_gateway_stage.dev.invoke_url}/movers"
}