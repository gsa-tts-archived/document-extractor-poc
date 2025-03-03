resource "aws_kms_key" "encryption" {
  description             = "Data encryption for ${local.project}"
  enable_key_rotation     = true
  deletion_window_in_days = 7
}
