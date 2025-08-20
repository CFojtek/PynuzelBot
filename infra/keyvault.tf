resource "azurerm_key_vault" "key_vault" {
    name                        = "${var.project_slug}-kv"
    location                    = var.location
    resource_group_name         = azurerm_resource_group.resource_group.name
    tenant_id                   = data.azurerm_client_config.current.tenant_id
    sku_name                    = "standard"
    soft_delete_retention_days  = 7

    tags = var.tags
}

resource "azurerm_key_vault_access_policy" "access_policy" {
    key_vault_id    = azurerm_key_vault.key_vault.id
    tenant_id       = data.azurerm_client_config.current.tenant_id
    object_id       = data.azurerm_client_config.current.object_id

    secret_permissions = ["Get", "List", "Set", "Delete"]
}