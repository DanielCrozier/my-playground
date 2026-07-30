output "resource_group_name" {
  description = "Name of the Azure Resource Group."
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "Name of the Azure Storage Account."
  value       = azurerm_storage_account.uploads.name
}

output "storage_container_name" {
  description = "Name of the blob container for uploads."
  value       = azurerm_storage_container.uploads.name
}

output "backend_url" {
  description = "HTTPS URL of the App Service backend."
  value       = "https://${azurerm_linux_web_app.backend.default_hostname}"
}

output "frontend_url" {
  description = "HTTPS URL of the Static Web App frontend."
  value       = "https://${azurerm_static_web_app.frontend.default_host_name}"
}

output "key_vault_name" {
  description = "Name of the Azure Key Vault."
  value       = azurerm_key_vault.main.name
}

output "static_web_app_api_key" {
  description = "Deployment API key for the Static Web App (used by GitHub Actions)."
  value       = azurerm_static_web_app.frontend.api_key
  sensitive   = true
}
