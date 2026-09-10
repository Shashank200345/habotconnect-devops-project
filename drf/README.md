# Task 3 — Schema Mapping & DCYN Validation (DRF)

**Submitted by:** [Your Full Name] — [Your Email] — [Your Phone Number]

## What "DCYN" means here

Deconstruct Complex [inputs into strict] Yes/No. Every field on the intake
form that could otherwise require a human to interpret intent is forced,
at `onboarding/serializers.py`, into an exact boolean or a fixed enum:

| Ambiguous source question | DCYN field | Type |
|---|---|---|
| "Does the child have a diagnosed learning difficulty?" | `has_diagnosed_learning_difficulty` | strict boolean |
| "What is the diagnosis?" (only meaningful if the above is true) | `diagnosis_type` | conditionally required, enforced in `validate()` |
| "Has the guardian consented?" | `guardian_consent_given` | strict boolean, **must be `true`** or the record is rejected outright |
| "Does the child need LSA support?" | `requires_lsa_support` | strict boolean |
| "How often?" | `preferred_session_frequency` | fixed enum (`daily`/`weekly`/`biweekly`/`monthly`) — never free text |

## Schema alignment with Pub/Sub → BigQuery

`onboarding/models.py`'s fields are identical, name-for-name, to
`terraform/schemas/student_onboarding_bq_schema.json`. This is deliberate:
the scenario in the brief (a schema mismatch broke downstream analytics)
happens when the app-side schema and the warehouse-side schema are edited
independently. Keeping one as the visible source of truth for the other
means a field rename has to break a test in **this** repo before it can
ever reach BigQuery.

## Proof this was actually run, not just written

```
$ python manage.py test onboarding -v 2
Ran 5 tests in 0.030s
OK
```

The 5 tests in `onboarding/tests.py` load the payloads in
`onboarding/sample_payloads/` and assert on real `serializer.errors`
output — including one case (`test_schema_mismatch_payload_is_rejected_on_every_bad_field`)
that initially exposed a wrong assumption on my part: I expected DRF's
object-level `validate()` to also flag `diagnosis_type` alongside the
enum/email errors in the same payload, but DRF only runs `validate()`
once every per-field check has passed — so that payload correctly
surfaces only the field-level errors, and the `diagnosis_type` rule is
verified independently in its own test. Left that correction in the test
file's comments rather than papering over it.

The code was also run through the same tools as the CI/CD gate in Task 2
(`black`, `flake8 --max-line-length=100`) with a clean exit — this
deliverable would pass its own pipeline.

## How to run this yourself

```bash
cd drf
pip install -r requirements.txt
python manage.py test onboarding -v 2
```
