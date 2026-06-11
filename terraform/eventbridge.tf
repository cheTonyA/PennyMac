resource "aws_cloudwatch_event_rule" "daily_stock_rule" {
  name                = "${var.project_name}-${var.environment}-daily-stock-rule"
  description         = "Runs stock processor after market close"
  schedule_expression = "cron(0 22 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_stock_rule.name
  target_id = "stockProcessorLambda"
  arn       = aws_lambda_function.stock_processor.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.stock_processor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_stock_rule.arn
}