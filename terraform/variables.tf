variable "project_id" {
  description = "GCP project ID that hosts the staging infrastructure."
  type        = string
}

variable "region" {
  description = "Default region for regional resources (bucket, dataset)."
  type        = string
  default     = "us-central1"
}

variable "app_engine_location_id" {
  description = "Immutable App Engine application location. Must match the existing application."
  type        = string
  default     = "us-central"
}

variable "environment" {
  description = "Deployment environment name, used in resource naming and labels."
  type        = string
  default     = "staging"
}

variable "raw_landing_writer_sa" {
  description = "Service account email allowed to WRITE to the D0 raw landing bucket (e.g. the ingestion job identity). Least-privilege: no other identity gets write access."
  type        = string
}

variable "staged_reader_sa" {
  description = "Service account email allowed to READ the D1 staged/enforced BigQuery dataset (e.g. the analytics/BI service identity)."
  type        = string
}

variable "schema_owner_sa" {
  description = "Service account email allowed to manage (create/alter) tables in D1. Distinct from the reader identity to enforce least privilege."
  type        = string
}

