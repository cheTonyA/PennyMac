resource "aws_amplify_app" "frontend" {
  name = "${var.project_name}-${var.environment}-frontend"

  environment_variables = {
    ENVIRONMENT = var.environment
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}