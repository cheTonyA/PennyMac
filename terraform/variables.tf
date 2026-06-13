variable "project_name" {
  description = "Project name"
  default     = "pennymac-stock-pipeline"
}

variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment"
  default     = "dev"
}

variable "massive_api_key" {
  description = "Massive API key"
  type        = string
  sensitive   = true
}

variable "watchlist" {
  description = "Stock tickers to track"
  type        = list(string)
  default     = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
}

variable "github_access_token" {
  description = "GitHub token for Amplify to access the repository"
  type        = string
  sensitive   = true
}

variable "alert_email" {
  description = "Email address for CloudWatch alarm notifications"
  type        = string
}