terraform {
  required_version = ">= 1.8"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 5.0.1"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Uncomment and populate before first production use.
  # backend "azurerm" {
  #   resource_group_name  = "tfstate-rg"
  #   storage_account_name = "tfstate<suffix>"
  #   container_name       = "tfstate"
  #   key                  = "my-playground.tfstate"
  # }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = true
    }
  }
  # Defaulting project to 'Test Subscription'
  subscription_id = "3f40ad49-3277-48ef-a0b2-c305bb75f575"
}

locals {
  common_tags = {
    environment = var.environment
    project     = var.project
    managed_by  = "terraform"
  }

  # Sanitised, lowercase prefix used in names that have character restrictions.
  name_prefix = lower(replace("${var.project}-${var.environment}", "_", "-"))
}

resource "azurerm_resource_group" "main" {
  name     = "${local.name_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}

# Short random suffix to guarantee globally unique names.
resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}
