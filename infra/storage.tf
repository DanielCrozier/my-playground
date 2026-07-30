resource "azurerm_storage_account" "uploads" {
  name                     = "${replace(local.name_prefix, "-", "")}${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # Disable public blob access – the backend uses the connection string.
  allow_nested_items_to_be_public  = false
  cross_tenant_replication_enabled = false

  blob_properties {
    delete_retention_policy {
      days = 7
    }
  }

  tags = local.common_tags
}

resource "azurerm_storage_container" "uploads" {
  name                  = "uploads"
  storage_account_name  = azurerm_storage_account.uploads.name
  container_access_type = "private"
}
