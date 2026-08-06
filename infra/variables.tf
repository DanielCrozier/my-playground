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
  default     = "eastus2"

  validation {
    condition = contains([
      "centralus",
      "eastus2",
      "westus2",
      "westeurope",
      "eastasia"
    ], lower(var.location))
    error_message = "location must be one of: centralus, eastus2, westus2, westeurope, eastasia."
  }
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

variable "backend_service_plan_sku" {
  description = "App Service Plan SKU for the backend (e.g. F1 for free tier, B1 for basic tier)."
  type        = string
  default     = "F1"

  validation {
    condition = contains([
      "f1",
      "b1"
    ], lower(var.backend_service_plan_sku))
    error_message = "backend_service_plan_sku must be one of: F1, B1."
  }
}
