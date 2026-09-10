# ---------------------------------------------------------------------------
# Least privilege: three distinct identities, none of which can do more than
# their one job. No "editor" or "owner" role is granted anywhere in this file.
# ---------------------------------------------------------------------------

# 1. Ingestion identity — WRITE-ONLY to D0. Cannot read D1, cannot manage IAM.
resource "google_storage_bucket_iam_member" "raw_landing_writer" {
  bucket = google_storage_bucket.d0_raw_landing.name
  role   = "roles/storage.objectCreator" # create-only, not objectAdmin — cannot overwrite or delete existing objects
  member = "serviceAccount:${var.raw_landing_writer_sa}"
}

# 2. Schema-owner identity — can manage D1 tables and is scoped to this dataset.
#    BigQuery dataset IAM does not support IAM conditions, so time-boxing must be
#    handled by an external access-review or scheduled binding removal process.
resource "google_bigquery_dataset_iam_member" "schema_owner" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.schema_owner_sa}"
}

# 3. Analytics/BI identity — READ-ONLY on D1. Cannot write, cannot alter schema.
#    Row-level scoping on top of this role is enforced separately in
#    schemas/bigquery_row_access_policy.sql — see terraform/README.md for why
#    row access policies are applied via SQL rather than a native TF resource.
resource "google_bigquery_dataset_iam_member" "staged_reader" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  role       = "roles/bigquery.dataViewer"
  member     = "serviceAccount:${var.staged_reader_sa}"
}
