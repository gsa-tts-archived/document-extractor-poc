resource "aws_sqs_queue" "queue_to_dynamo" {
  name = "${local.project}-${var.environment}-to-dynamodb"

  kms_master_key_id = aws_kms_key.encryption.id
}
