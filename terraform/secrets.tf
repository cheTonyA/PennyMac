resource "aws_secretsmanager_secret" "massive_api_key" {
  name        = "${var.project_name}/${var.environment}/massive-api-key"
  description = "Massive API key for stock pipeline"
}