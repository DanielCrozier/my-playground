data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                       = "${replace(local.name_prefix, "-", "")}kv${random_string.suffix.result}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  rbac_authorization_enabled = true
  sku_name                   = "standard"
  tenant_id                  = data.azurerm_client_config.current.tenant_id

  tags = local.common_tags
}

resource "azurerm_key_vault_secret" "storage_connection_string" {
  name         = "AZURE-STORAGE-CONNECTION-STRING"
  value        = azurerm_storage_account.uploads.primary_connection_string
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [time_sleep.wait_for_kv_secret_rbac]

  tags = local.common_tags
}

# Grant the backend managed identity read access through RBAC.
resource "azurerm_role_assignment" "backend_secret_reader" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_web_app.backend.identity[0].principal_id
}

# Grant Terraform permission to manage the secret via RBAC.
resource "azurerm_role_assignment" "deployer_secret_manager" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

# RBAC permissions can take time to propagate to the Key Vault data plane.
resource "time_sleep" "wait_for_kv_secret_rbac" {
  depends_on      = [azurerm_role_assignment.deployer_secret_manager]
  create_duration = "60s"
}
