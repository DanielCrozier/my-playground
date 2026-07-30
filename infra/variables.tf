variable "project" {
  description = "Short project identifier used in resource names."
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "eastus"
}

variable "allowed_origins" {
  description = "Comma-separated list of CORS origins allowed by the backend."
  type        = string
  default     = "*"
}

variable "max_upload_size_bytes" {
  description = "Maximum allowed upload size in bytes."
  type        = number
  default     = 10485760 # 10 MB
}
