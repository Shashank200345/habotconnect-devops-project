# Task 1 — Secure Staging Infrastructure (Terraform)

**Submitted by:** SHASHANK DWIVEDI — dwivedishashank413@gmail.com — +917080498684

## What this provisions

| Resource | File | Purpose |
|---|---|---|
| `google_storage_bucket.d0_raw_landing` | `main.tf` | D0 — unvalidated raw landing zone. Versioned, 30-day lifecycle, no public access. |
| `google_bigquery_dataset.d1_staged_enforced` + `google_bigquery_table.student_onboarding` | `main.tf` | D1 — schema-enforced destination. Table schema in `schemas/student_onboarding_bq_schema.json` mirrors the DRF serializer field-for-field so the two cannot silently drift apart. |
| IAM bindings | `iam.tf` | Three distinct, least-privilege identities — write-only ingestion, dataset-scoped schema owner, and read-only analytics. No identity receives a project-level `owner` or `editor` role from this module. |
| App Engine application | `main.tf` | Existing App Engine application adopted into Terraform state and managed without recreation. |
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
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
```

`bq` CLI must be authenticated in whatever environment runs `apply` (operator
machine or CI runner), since `rls_apply.tf` invokes it after the table exists.
The existing App Engine application was imported with:

```powershell
terraform import -var-file="terraform.tfvars" `
  google_app_engine_application.default habot-devops-staging
```

## Verification performed

Terraform was applied successfully to project `habot-devops-staging`.
The live plan reports `No changes. Your infrastructure matches the
configuration.` The App Engine application is `SERVING`, and the active Row-
Level Security policy is `lsa_support_only` with filter
`requires_lsa_support = TRUE` for the staged-reader service account.

BigQuery dataset IAM conditions are not supported at this scope, so the
schema-owner binding is dataset-scoped and time-boxing must be handled by an
external access-review process.
