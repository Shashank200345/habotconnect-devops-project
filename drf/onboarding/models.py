import uuid

from django.db import models


class SessionFrequency(models.TextChoices):
    """Fixed enum - never free text. Part of eliminating human judgment
    from the intake path per the Poka-Yoke brief."""

    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    BIWEEKLY = "biweekly", "Biweekly"
    MONTHLY = "monthly", "Monthly"


class StudentOnboarding(models.Model):
    """Enforced record promoted from D0 raw landing into D1 staged/enforced.

    Field set is kept identical to
    terraform/schemas/student_onboarding_bq_schema.json so the DRF layer and
    the BigQuery streaming sink can never silently drift out of sync.
    """

    record_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()

    # DCYN fields - every one of these collapses an originally ambiguous /
    # free-text intake question into a strict boolean, so nothing downstream
    # has to interpret intent.
    has_diagnosed_learning_difficulty = models.BooleanField()
    diagnosis_type = models.CharField(max_length=80, blank=True, null=True)
    guardian_consent_given = models.BooleanField()
    requires_lsa_support = models.BooleanField()

    preferred_session_frequency = models.CharField(
        max_length=10, choices=SessionFrequency.choices
    )
    contact_email = models.EmailField()
    submitted_at = models.DateTimeField(
        auto_now_add=True
    )  # server-set, never trusted from payload

    def __str__(self):
        return f"{self.full_name} ({self.record_id})"
