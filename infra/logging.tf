resource "azurerm_log_analytics_workspace" "log_analytics_workspace" {
  name                = "${var.project_slug}-law"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}