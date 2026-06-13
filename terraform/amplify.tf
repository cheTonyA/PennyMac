resource "aws_amplify_app" "frontend" {
  name         = "${var.project_name}-${var.environment}-frontend"
  repository   = "https://github.com/cheTonyA/PennyMac"
  access_token = var.github_access_token

  build_spec = <<-EOT
version: 1
applications:
  - appRoot: frontend
    frontend:
      phases:
        build:
          commands: []
      artifacts:
        baseDirectory: .
        files:
          - '**/*'
      cache:
        paths: []
EOT

  environment_variables = {
    ENVIRONMENT = var.environment
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_amplify_branch" "main" {
  app_id            = aws_amplify_app.frontend.id
  branch_name       = "main"
  enable_auto_build = true
  framework         = "Web"

  stage = "PRODUCTION"
}