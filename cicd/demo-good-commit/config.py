import os

# Compliant version: no secret is ever hardcoded. Values are read from the
# environment (populated from GCP Secret Manager / GitHub Actions secrets
# at deploy time), so there is nothing here for a secret scanner to flag
# and nothing here for a human to accidentally leave in the repo.

STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


def get_payment_client():
    return {"api_key": STRIPE_API_KEY}
