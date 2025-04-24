resource "aws_secretsmanager_secret" "private_key" {
  name = "${local.project}-${var.environment}-private-key"
}

resource "aws_secretsmanager_secret" "public_key" {
  name = "${local.project}-${var.environment}-public-key"
}

resource "aws_secretsmanager_secret" "username" {
  name = "${local.project}-${var.environment}-username"
}

resource "aws_secretsmanager_secret" "password" {
  name = "${local.project}-${var.environment}-password"
}
