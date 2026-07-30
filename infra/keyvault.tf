data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                = "${local.name_prefix}-kv-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku_name            = "standard"
  tenant_id           = data.azurerm_client_config.current.tenant_id

  # Only the deploying principal (pipeline SP / developer) can manage secrets.
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete",
      "Purge",
      "Recover",
    ]
  }

  # App Service managed identity reads the storage connection string.
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azurerm_linux_web_app.backend.identity[0].principal_id

    secret_permissions = [
      "Get",
      "List",
    ]
  }

  tags = local.common_tags
}

resource "azurerm_key_vault_secret" "storage_connection_string" {
  name         = "AZURE-STORAGE-CONNECTION-STRING"
  value        = azurerm_storage_account.uploads.primary_connection_string
  key_vault_id = azurerm_key_vault.main.id

  tags = local.common_tags
}
