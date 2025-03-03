resource "aws_dynamodb_table" "extract_table" {
  name     = "${local.project}-${var.environment}-text-extract"
  hash_key = "document_id"

  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "document_id"
    type = "S"
  }
}
