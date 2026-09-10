# Task 2 — Poka-Yoke Automated CI/CD Build Gate

**Submitted by:** [Your Full Name] — [Your Email] — [Your Phone Number]

## How the fail-closed mechanism works

`.github/workflows/ci-cd-gate.yml` defines three jobs: `lint`, `secret-scan`,
and `deploy`. The `deploy` job declares `needs: [lint, secret-scan]`. In
GitHub Actions, a job listed in `needs` **must succeed** before the
dependent job is even scheduled — there is no code path where `deploy` runs
after either gate fails. That is the entire mechanism; nothing about it
depends on a human remembering to check a status before merging.

- **Lint gate:** `flake8` + `black --check` on the Django backend,
  `eslint --max-warnings=0` on the React frontend when present.
- **Secret-scan gate:** `gitleaks/gitleaks-action@v2`, which scans the full
  diff and exits non-zero on any detected credential pattern.

## Proof this actually blocks bad commits — reproduced locally

Rather than only asserting the gate works, `demo-gate-evidence.log` captures
a real run of both underlying tools:

- `demo-bad-commit/leaked_config.py` — a synthetic (fake) hardcoded Stripe
  key and DB URL, reproducing the exact scenario in the brief. Running the
  real `gitleaks` binary against it returns **exit code 1** with the exact
  finding (rule `stripe-access-token`, line 6).
- `demo-bad-commit/bad_format.py` — intentionally malformatted code. Running
  the real `flake8` against it returns **exit code 1** with 5 violations.
- `demo-good-commit/config.py` — the compliant fix (secrets read from
  environment variables, populated from GCP Secret Manager / Actions
  secrets at deploy time). Both tools return **exit code 0** against it.

This was run directly in this environment, not simulated — see
`demo-gate-evidence.log` for the raw tool output. On a real GitHub Actions
run, a non-zero exit from either tool fails that job, which — via `needs:`
— prevents `deploy` from ever starting.

## To reproduce yourself against a real PR

1. Push a branch containing `demo-bad-commit/leaked_config.py` into the repo
   root and open a PR — the `secret-scan` job will fail and the checks tab
   will show it red.
2. Screenshot the failed check + the `deploy` job showing "skipped" (not
   "failed" — skipped because its `needs:` condition was never met) for the
   presentation.
