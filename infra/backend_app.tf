resource "azurerm_service_plan" "backend" {
  name                = "${local.name_prefix}-asp"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "B1"

  tags = local.common_tags
}

resource "azurerm_linux_web_app" "backend" {
  name                = "${local.name_prefix}-api-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.backend.id

  https_only = true

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      python_version = "3.12"
    }
    always_on = true
  }

  app_settings = {
    # Key Vault reference – resolved at runtime, never stored in plain text.
    "AZURE_STORAGE_CONNECTION_STRING" = "@Microsoft.KeyVault(VaultName=${azurerm_key_vault.main.name};SecretName=${azurerm_key_vault_secret.storage_connection_string.name})"
    "AZURE_STORAGE_CONTAINER_NAME"    = azurerm_storage_container.uploads.name
    "ALLOW_ORIGINS"                   = var.allowed_origins
    "MAX_UPLOAD_SIZE_BYTES"           = tostring(var.max_upload_size_bytes)
    "SCM_DO_BUILD_DURING_DEPLOYMENT"  = "true"
    "WEBSITE_RUN_FROM_PACKAGE"        = "1"
  }

  tags = local.common_tags
}
