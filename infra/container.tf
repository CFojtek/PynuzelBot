resource "azurerm_container_registry" "container_registry" {
    name                = "${var.project_slug}cr"
    location            = var.location
    resource_group_name = azurerm_resource_group.resource_group.name
    sku                 = "Basic"
    admin_enabled       = true

    tags = var.tags
}

resource "azurerm_container_group" "container_group" {
    name                = "${var.project_slug}-cg"
    location            = var.location
    resource_group_name = azurerm_resource_group.resource_group.name
    
    os_type             = "Linux"
    sku                 = "Standard"
    ip_address_type     = "Public"
    dns_name_label      = "${var.project_slug}-dns"

    tags                = var.tags
    depends_on          = [ azurerm_container_registry.container_registry ]

    container {
        name    = "signal-bot"
        image   = "${azurerm_container_registry.container_registry.login_server}/${var.image_name_signal_bot}"
        cpu     = 1
        memory  = 1.5
        

        environment_variables = {
          SIGNAL_SERVICE    = "localhost:8080" # Azure container groups use localhost for inter-container communication
          ENV               = var.env
        }

        secure_environment_variables = {
          PHONE_NUMBER     = data.azurerm_key_vault_secret.phone_number.value
          USER_GROUP       = data.azurerm_key_vault_secret.user_group.value
          ADMIN_GROUP      = data.azurerm_key_vault_secret.admin_group.value
          AIRTABLE_TOKEN   = data.azurerm_key_vault_secret.airtable_token.value
          AIRTABLE_BASE_ID = data.azurerm_key_vault_secret.airtable_base_id.value
        }
    }

    container {
        name = "signal-cli"
        image = "${azurerm_container_registry.container_registry.login_server}/${var.image_name_signal_cli}"
        cpu = 1
        memory = 2

        environment_variables = {
          MODE = "json-rpc"
        }

        ports {
            port     = 8080
            protocol = "TCP"
        }

        volume {
          name = "signal-cli-config"
          mount_path = "/home/.local/share/signal-cli"
          read_only = false

          storage_account_name = azurerm_storage_account.storage_account.name
          storage_account_key  = azurerm_storage_account.storage_account.primary_access_key
          share_name           = azurerm_storage_share.storage_share.name
        }
    }

    image_registry_credential {
      server = azurerm_container_registry.container_registry.login_server
      username = azurerm_container_registry.container_registry.admin_username
      password = azurerm_container_registry.container_registry.admin_password
    }

    diagnostics {
      log_analytics {
          log_type      = "ContainerInsights"
          workspace_id  = azurerm_log_analytics_workspace.log_analytics_workspace.workspace_id
          workspace_key = azurerm_log_analytics_workspace.log_analytics_workspace.primary_shared_key
        }
    }
}
