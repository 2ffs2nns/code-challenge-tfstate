provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "tfstate_bucket" {
  #checkov:skip=CKV_GCP_62:Bucket should log access
  name          = "${var.project_id}-tfstate"
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = true

  versioning {
    enabled = true
  }

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}

resource "google_service_account" "terraform" {
  account_id                   = var.service_account_name
  display_name                 = var.service_account_name
  create_ignore_already_exists = var.skip_service_account_creation
}

resource "google_storage_bucket_iam_member" "tf_backend_storage_admin" {
  bucket = google_storage_bucket.tfstate_bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.terraform.email}"
}
