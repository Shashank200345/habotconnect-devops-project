# DEMO ONLY — this file intentionally reproduces the scenario in the brief:
# "a junior developer has pushed an update that... left unencrypted API
# credentials in raw application code." This is a synthetic, fake key used
# only to prove the secret-scan gate catches and blocks this pattern.

# Deliberately invalid placeholder. Use a local-only generated fixture when
# demonstrating a real secret-scan failure; never commit credential-shaped data.
STRIPE_API_KEY = "REPLACE_WITH_LOCAL_TEST_SECRET"

DATABASE_URL = "postgres://admin:SuperSecretPass123@10.0.0.5:5432/habotconnect"


def get_payment_client():
    return {"api_key": STRIPE_API_KEY}
