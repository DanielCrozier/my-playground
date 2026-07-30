resource "azurerm_static_web_app" "frontend" {
  name                = "${local.name_prefix}-swa-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku_tier            = "Free"
  sku_size            = "Free"

  tags = local.common_tags
}
