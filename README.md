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
│   ├── demo-bad-commit/        intentionally non-compliant files (secret + bad formatting)
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

## What's real vs. what's documented-but-not-executable here

To be direct about verification, per the brief's emphasis on rigor and zero
placeholders:

- **Executed and verified in this environment:** the Django/DRF test suite
  (5/5 passing against real sample payloads), the `gitleaks` secret scan
  and `flake8` lint checks (run with the real tools against the demo
  commits — see `cicd/demo-gate-evidence.log`), and HCL syntax validation
  of every Terraform file.
- **Not executed here (no GCP credentials in this environment):** an actual
  `terraform apply` against a live GCP project, and a live GitHub Actions
  run of the full workflow. Both are described precisely enough to run
  as-is once pointed at real credentials — `terraform/README.md` and
  `cicd/README.md` give the exact commands. Recommend running both for
  real before the panel presentation and keeping screenshots as evidence.

## Before you submit

- [ ] Fill in your actual name/email/phone wherever `[Your ... ]` appears (every README)
- [ ] Get the Leadership Principles + Values PDFs from HR if you don't have them yet
- [ ] Run `terraform plan` against a real GCP project and screenshot the output
- [ ] Push the `demo-bad-commit` files to a branch and screenshot the failed GitHub Actions check + the skipped `deploy` job
- [ ] Build the 15-slide deck in `docs/` (architecture overview + logic flow + the fail-closed proof)
- [ ] Confirm every doc uses full forms only — no abbreviations, no placeholders left behind
- [ ] Submit via the Google Form before 13 September 2026

Pipeline smoke test.
