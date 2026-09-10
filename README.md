# HabotConnect Hiring Project — Junior Cloud & DevOps Engineer

**Submitted by:** SHASHANK DWIVEDI — dwivedishashank413@gmail.com — +917080498684
## Folder architecture

```
habotconnect-project/
├── terraform/                  Task 1 — IaC for D0 raw landing + D1 staged/enforced
│   ├── main.tf
│   ├── variables.tf
│   ├── iam.tf
│   ├── outputs.tf
│   ├── rls_apply.tf
│   ├── schemas/
│   │   ├── student_onboarding_bq_schema.json   (shared with drf/onboarding/models.py)
│   │   └── bigquery_row_access_policy.sql
│   └── README.md
├── cicd/                       Task 2 — fail-closed Poka-Yoke build gate
│   ├── .github/workflows/ci-cd-gate.yml
│   ├── demo-bad-commit/        intentionally non-compliant files (local-only secret test + bad formatting)
│   ├── demo-good-commit/       the compliant fix, for comparison
│   ├── demo-gate-evidence.log  real tool output proving the gate blocks the bad commit
│   └── README.md
├── drf/                        Task 3 — DCYN serializer + schema validation
│   ├── config/, manage.py      minimal Django project (sqlite, for local testing only)
│   ├── onboarding/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py            5 passing tests, run against real sample payloads
│   │   └── sample_payloads/
│   ├── requirements.txt
│   └── README.md
└── docs/                       15-slide presentation deck goes here
```

## Project overview

This project is a production-style deployment and automation blueprint for a
student onboarding platform. It demonstrates how validated Django data moves
through a protected Google Cloud pipeline:

```text
Student onboarding request
        |
        v
Django REST Framework validation
        |
        v
D0 Google Cloud Storage raw landing
        |
        v
D1 BigQuery staged and enforced table
        |
        v
Row-Level Security filtered analytics access
```

The application is deployed to Google App Engine and uses Google Secret
Manager for its production Django secret key. Terraform manages the existing
App Engine application, storage bucket, BigQuery resources, and IAM bindings.

## Security design

- The raw landing bucket blocks public access, uses uniform bucket-level
  access, enables object versioning, and deletes transient objects after 30
  days.
- The raw landing writer can create objects but cannot read, overwrite, or
  delete existing objects.
- The staged reader has read-only BigQuery access and is restricted by the
  `lsa_support_only` Row-Level Security policy.
- Schema-owner access is limited to the staged dataset. Google Cloud does not
  support IAM conditions on BigQuery dataset bindings, so time-boxing must be
  handled through an external access-review process.
- GitHub Actions authenticates with a dedicated deployment identity, and
  deployment is reachable only after linting and secret scanning succeed.

## Verification status

To be direct about verification, per the brief's emphasis on rigor and zero
placeholders:

- **Local checks passed:** 5 Django/DRF tests, Black formatting, Flake8
  linting, Terraform formatting and validation, and Gitleaks scanning.
- **Live GCP checks passed:** Terraform apply, App Engine deployment,
  BigQuery Row-Level Security verification, and App Engine health checks.
- **Live GitHub Actions checks passed:** lint gate, secret-scan gate, and
  App Engine deployment through the root workflow at
  `.github/workflows/ci-cd-gate.yml`.
- **Secret-scan evidence boundary:** the credential-shaped failure fixture is
  generated locally and is never pushed to GitHub. The committed repository
  is clean and passes Gitleaks.

## Live deployment

- Google Cloud project: `habot-devops-staging`
- App Engine service: `default`
- App Engine URL: https://habot-devops-staging.uc.r.appspot.com
- BigQuery dataset: `d1_staged_enforced`
- BigQuery table: `student_onboarding`
- Row-Level Security policy: `lsa_support_only`
- Raw landing bucket: `habot-devops-staging-d0-raw-landing-staging`

The repository contains the implementation, test fixtures, workflow
configuration, and reproducible local evidence for all three assignment
tasks. The presentation materials are maintained separately in `docs/`.
