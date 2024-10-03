variable "project_id" {
  description = "Default gcloud project to launch this cluster into"
  type        = string
}

variable "region" {
  default     = "us-central1"
  description = "Default region"
  type        = string
}

variable "service_account_name" {
  default     = "terraform"
  description = "gcloud service account name to use."
  type        = string
}

variable "skip_service_account_creation" {
  default     = true
  description = "Ignore creating new service account if the name already exists."
  type        = bool
}
