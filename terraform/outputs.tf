output "d0_raw_landing_bucket" {
  description = "Name of the D0 raw landing bucket."
  value       = google_storage_bucket.d0_raw_landing.name
}

output "d1_dataset_id" {
  description = "BigQuery dataset ID for D1 staged/enforced data."
  value       = google_bigquery_dataset.d1_staged_enforced.dataset_id
}

output "d1_student_onboarding_table" {
  description = "Fully qualified table ID for the enforced student onboarding table."
  value       = "${var.project_id}.${google_bigquery_dataset.d1_staged_enforced.dataset_id}.${google_bigquery_table.student_onboarding.table_id}"
}
