variable "project_name" {
  description = "Project name, typically the git repository"
  type        = string
}

variable "gcloud_env" {
  description = "Environment to deploy into. ie production, staging, development"
  type        = string
}

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
