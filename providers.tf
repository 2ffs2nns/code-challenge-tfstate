terraform {
  required_version = ">= 1.9"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.40"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
