resource "aws_dynamodb_table" "stock_results" {
  name         = "${var.project_name}-${var.environment}-stock-results"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "trade_date"

  attribute {
    name = "trade_date"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}