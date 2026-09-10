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

## Before you submit

- [x] Fill in your actual name, email, and phone in every README
- [ ] Get the Leadership Principles + Values PDFs from Human Resources if you don't have them yet
- [x] Run `terraform plan` against the live GCP project and verify no drift
- [x] Run the compliant GitHub Actions pipeline and capture the successful deployment evidence
- [ ] Capture a failed lint-branch run showing the skipped deployment job
- [ ] Build the 15-slide deck in `docs/` (architecture overview + logic flow + the fail-closed proof)
- [x] Confirm the project READMEs contain no personal-information placeholders
- [ ] Submit via the Google Form before 13 September 2026

Live App Engine URL: https://habot-devops-staging.uc.r.appspot.com
