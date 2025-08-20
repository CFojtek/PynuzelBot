resource "azurerm_resource_group" "resource_group" {
    name        = "${var.project_slug}-rg"
    location    = var.location
  
    tags = var.tags
}
