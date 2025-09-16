resource "azurerm_storage_account" "storage_account" {
  name                     = "${var.project_slug}sa"
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_share" "storage_share" {
  name                 = "signal-cli-config"
  storage_account_id = azurerm_storage_account.storage_account.id
  quota                = 10
}
