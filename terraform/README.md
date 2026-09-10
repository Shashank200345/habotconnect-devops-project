# Task 1 — Secure Staging Infrastructure (Terraform)

**Submitted by:** [Your Full Name] — [Your Email] — [Your Phone Number]

## What this provisions

| Resource | File | Purpose |
|---|---|---|
| `google_storage_bucket.d0_raw_landing` | `main.tf` | D0 — unvalidated raw landing zone. Versioned, 30-day lifecycle, no public access. |
| `google_bigquery_dataset.d1_staged_enforced` + `google_bigquery_table.student_onboarding` | `main.tf` | D1 — schema-enforced destination. Table schema in `schemas/student_onboarding_bq_schema.json` mirrors the DRF serializer field-for-field so the two cannot silently drift apart. |
| IAM bindings | `iam.tf` | Three distinct, least-privilege identities — write-only ingestion, time-boxed schema owner, read-only analytics. No identity holds `editor` or `owner`. |
| Row access policy | `schemas/bigquery_row_access_policy.sql` + `rls_apply.tf` | Row-Level Security restricting the analytics identity to rows where `requires_lsa_support = TRUE`. |

## Why RLS is applied via SQL, not a single native resource

Terraform provider support for native BigQuery row access policies varies by
pinned provider version. Rather than assume a resource is available and risk
shipping an unenforced policy that silently no-ops, this module applies the
policy explicitly through a `null_resource` + `local-exec` calling `bq query`
(`rls_apply.tf`), with the actual policy kept in a reviewable `.sql` file.
If your environment's provider version does expose the native resource, this
SQL is a documented, drop-in replacement path — noted here rather than
assumed silently.

## How to run this

```bash
cd terraform
terraform init
terraform plan  \
  -var="project_id=YOUR_GCP_PROJECT" \
  -var="raw_landing_writer_sa=ingestion@YOUR_GCP_PROJECT.iam.gserviceaccount.com" \
  -var="staged_reader_sa=analytics@YOUR_GCP_PROJECT.iam.gserviceaccount.com" \
  -var="schema_owner_sa=schema-owner@YOUR_GCP_PROJECT.iam.gserviceaccount.com"
terraform apply  # add the same -var flags
```

`bq` CLI must be authenticated in whatever environment runs `apply` (operator
machine or CI runner), since `rls_apply.tf` shells out to it.

## Verification performed

All five `.tf` files were parsed with an HCL2 parser to confirm they are
syntactically valid (`OK` on `main.tf`, `variables.tf`, `iam.tf`,
`outputs.tf`, `rls_apply.tf`). A live `terraform plan` against a real GCP
project was not run in this environment — no GCP credentials are available
here — so this module has not yet been apply-tested end to end. Recommend
running `terraform plan` yourself against a real project before the
presentation and screenshotting the output as evidence.
