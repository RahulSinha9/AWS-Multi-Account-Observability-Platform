variable "aws_region" {
  type = string
  default = "us-east-1"
}
variable "role_name" {
  type = string
  default = "central-observability-read-role"
}
variable "observability_account_id" {
  type = string
  description = "Central observability account allowed to assume the role."
}
