resource "azurerm_key_vault" "key_vault" {
    name                        = "${var.project_slug}-kv"
    location                    = var.location
    resource_group_name         = azurerm_resource_group.resource_group.name
    tenant_id                   = var.tenant_id
    sku_name                    = "standard"
    soft_delete_retention_days  = 7

    tags = var.tags
}

resource "azurerm_key_vault_access_policy" "access_policy" {
    key_vault_id    = azurerm_key_vault.key_vault.id
    tenant_id       = var.tenant_id
    object_id       = var.object_id

    secret_permissions = ["Get", "List", "Set", "Delete"]
}

data "azurerm_key_vault_secret" "phone_number" {
    name         = "phone-number"
    key_vault_id = azurerm_key_vault.key_vault.id
}

data "azurerm_key_vault_secret" "user_group" {
    name         = "user-group"
    key_vault_id = azurerm_key_vault.key_vault.id
}

data "azurerm_key_vault_secret" "admin_group" {
    name         = "admin-group"
    key_vault_id = azurerm_key_vault.key_vault.id
}

data "azurerm_key_vault_secret" "airtable_token" {
    name         = "airtable-token"
    key_vault_id = azurerm_key_vault.key_vault.id
}

data "azurerm_key_vault_secret" "airtable_base_id" {
    name         = "airtable-base-id"
    key_vault_id = azurerm_key_vault.key_vault.id
}