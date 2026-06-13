terraform {
  backend "s3" {
    bucket       = "pennymac-stock-pipeline-tfstate-629490206604"
    key          = "pennymac-stock-pipeline/dev/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}