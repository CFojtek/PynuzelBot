variable "project_slug" {
    description = "Project slug used for naming"
    type        = string
}

variable "location" {
    description = "Azure region name"
    type        = string
    default     = "West Europe"
}

variable "env" {
    description = "Environment name (e.g., dev, prod)"
    type        = string
    default     = "dev"
}

variable tenant_id {
    description = "Azure Tenant ID"
    type        = string
}

variable subscription_id {
    description = "Azure Subscription ID"
    type        = string
}

variable object_id {
    description = "Object ID of the user/service principal for Key Vault access"
    type        = string
}

variable "image_name_signal_cli" {
    description = "Image name in the container registry of the signal-cli"
    type        = string
}

variable "image_name_signal_bot" {
    description = "Image name in the container registry of the signal-bot"
    type        = string
}

variable "tags" {
    description = "Tags to apply to resources"
    type        = map(string)
    default     = {
        environment = "dev"
        project     = "my_project"
    }
}