variable "region" {
  description = "Region for placing all resources"
}

variable "instance_type" {
  description = "Instance type"
}

variable "product_name" {
  description = "Product name used in resource naming"
  default     = "calc-visualizer"
}
