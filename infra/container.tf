resource "azurerm_container_registry" "container_registry" {
    name                = "${var.project_slug}-cr"
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
    sku                 = "Basic"
    ip_address_type     = "Public"
    dns_name_label      = "${var.project_slug}-dns"

    tags                = var.tags

    container {
        name    = "${var.project_slug}"
        image   = "${azurerm_container_registry.container_registry.login_server}/${var.image_name}:latest"
        cpu     = 1
        memory  = 1.5

        environment_variables = {
          SIGNAL_SERVICE    = "signal-cli:8080"
          ENV               = var.env
        }

        secure_environment_variables = {
          # TODO add secret env variables here from key vault
        }

        ports {
            port     = 8080
            protocol = "TCP"
        }
    }

    container {
        name = "signal-cli"
        image = "${azurerm_container_registry.container_registry.login_server}/signal-cli:latest"
        cpu = 1
        memory = 1.5

        environment_variables = {
          MODE = "json-rcp"
        }

        ports {
            port     = 8080
            protocol = "TCP"
        }
    }

    image_registry_credential {
      server = azurerm_container_registry.container_registry.login_server
      username = azurerm_container_registry.container_registry.admin_username
      password = azurerm_container_registry.container_registry.admin_password
    }
}
