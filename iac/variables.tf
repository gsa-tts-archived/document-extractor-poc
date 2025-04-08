variable "region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type = string
}

variable "w2_textract_adapter_id_0" {
  type      = string
  nullable  = false
  sensitive = true
}

variable "w2_textract_adapter_id_1" {
  type      = string
  nullable  = false
  sensitive = true
}

variable "dd214_textract_adapter_id" {
  type      = string
  nullable  = false
  sensitive = true
}

# variable "ten99_textract_adapter_id" {
#   type = string
#   nullable  = true
#   sensitive = true
# }

# variable "map_from_gha" {
#   type = map
# }
