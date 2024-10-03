terraform {
  backend "gcs" {
    # NOTE: the gcs_bucket_name output from this repo.
    # however, this is a chicken/egg, create the bucket
    # before adding this backend. Update w/your specific
    # gcloud_env and project_name values then run
    # terraform init -backend-config='prefix=terraform/<gcloud_env>/<project_name>/'
    bucket = "code-challenge-62079-tfstate"
  }
}
