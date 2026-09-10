terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ---------------------------------------------------------------------------
# D0 — RAW LANDING (GCS)
# Unvalidated data lands here first. Nothing downstream reads from D0 directly;
# it exists so a bad payload never touches an enforced table.
# ---------------------------------------------------------------------------
resource "google_storage_bucket" "d0_raw_landing" {
  name                        = "${var.project_id}-d0-raw-landing-${var.environment}"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true # disables legacy per-object ACLs; IAM is the single source of truth

  public_access_prevention = "enforced" # hard block on public exposure, cannot be overridden by a future ACL change

  versioning {
    enabled = true # a bad object can be recovered instead of silently overwriting good data
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete" # raw landing is transient — data is promoted to D1 or discarded, never kept indefinitely
    }
  }

  labels = {
    environment = var.environment
    data_stage  = "d0-raw"
    managed_by  = "terraform"
  }
}

# ---------------------------------------------------------------------------
# D1 — STAGED / ENFORCED (BigQuery)
# Only data that has passed schema + validation (see drf/onboarding/serializers.py)
# is promoted here. This dataset backs the Pub/Sub streaming sink.
# ---------------------------------------------------------------------------
resource "google_bigquery_dataset" "d1_staged_enforced" {
  dataset_id                  = "d1_staged_enforced"
  friendly_name               = "D1 Staged Enforced"
  description                 = "Validated, schema-enforced student onboarding records. Fed by the Pub/Sub streaming sink after DRF serializer validation."
  location                    = var.region
  default_table_expiration_ms = null # enforced data is durable, unlike D0

  labels = {
    environment = var.environment
    data_stage  = "d1-staged"
    managed_by  = "terraform"
  }
}

# Table schema intentionally mirrors the DRF serializer output field-for-field
# (see drf/onboarding/schema/onboarding_schema.json) so the two never drift apart.
resource "google_bigquery_table" "student_onboarding" {
  dataset_id          = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id            = "student_onboarding"
  deletion_protection = true

  schema = file("${path.module}/schemas/student_onboarding_bq_schema.json")

  labels = {
    environment = var.environment
    managed_by  = "terraform"
  }
}
