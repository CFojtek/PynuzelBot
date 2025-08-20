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

variable "image_name" {
    description = "Image name in the container registry"
    type        = string
}

variable "tags" {
    description = "Tags to apply to resources"
    type        = map(string)
    default     = {
        environment = var.env
        project     = var.project_slug
    }
}