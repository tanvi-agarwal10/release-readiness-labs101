variable "aws_secret_key" {
  type        = string
  description = "AWS secret access key provided securely at runtime via environment or secret manager"
  sensitive   = true
  default     = null
}
