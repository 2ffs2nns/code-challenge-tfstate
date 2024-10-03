output "gcs_bucket_name" {
  value = google_storage_bucket.tfstate_bucket.name
}
