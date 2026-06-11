data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "stock_processor" {
  function_name = "${var.project_name}-${var.environment}-processor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  timeout       = 30

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      MASSIVE_API_KEY = var.massive_api_key
      DYNAMODB_TABLE  = aws_dynamodb_table.stock_results.name
      WATCHLIST       = join(",", var.watchlist)
    }
  }
}

resource "aws_lambda_function" "api_lambda" {
  function_name = "${var.project_name}-${var.environment}-api"

  role    = aws_iam_role.lambda_role.arn
  handler = "api_handler.lambda_handler"
  runtime = "python3.12"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  timeout = 30

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.stock_results.name
    }
  }
}