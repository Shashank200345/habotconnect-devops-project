# Task 2 — Poka-Yoke Automated CI/CD Build Gate

**Submitted by:** SHASHANK DWIVEDI — dwivedishashank413@gmail.com — +917080498684

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

- `demo-bad-commit/leaked_config.py` — a sanitized fixture documenting the
  scenario in the brief. A credential-shaped failure file is generated only
  in a local temporary directory and is never pushed to GitHub.
- `demo-bad-commit/bad_format.py` — intentionally malformatted code. Running
  the real `flake8` against it returns **exit code 1** with 5 violations.
- `demo-good-commit/config.py` — the compliant fix (secrets read from
  environment variables, populated from GCP Secret Manager / Actions
  secrets at deploy time). Both tools return **exit code 0** against it.

— prevents `deploy` from ever starting.
This was run directly in this environment, not simulated — see
`demo-gate-evidence.log` for the raw tool output. The live GitHub Actions
workflow also completed the lint gate, secret-scan gate, and App Engine
deployment successfully. On any run, a non-zero exit from either tool fails
that job, which — via `needs:` — prevents `deploy` from ever starting.

## To reproduce yourself against a real PR

1. Create a temporary local credential-shaped file and run Gitleaks against
  it. Never push that file to GitHub because repository secret scanning will
  block the push.
2. Push a branch with a deliberately malformed Python file — without any
  secret — and open a pull request. The `lint` job will fail and the checks
  tab will show it red.
3. Screenshot the failed check + the `deploy` job showing "skipped" (not
   "failed" — skipped because its `needs:` condition was never met) for the
   presentation.
