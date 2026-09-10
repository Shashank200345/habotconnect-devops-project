import json
import os

from django.test import TestCase

from .serializers import StudentOnboardingSerializer

PAYLOAD_DIR = os.path.join(os.path.dirname(__file__), "sample_payloads")


def load_payload(filename):
    with open(os.path.join(PAYLOAD_DIR, filename)) as f:
        return json.load(f)


class StudentOnboardingSerializerTests(TestCase):
    """Proves the DCYN validation rules actually hold, using the same
    sample payloads referenced in the Task 3 README."""

    def test_valid_payload_is_accepted(self):
        data = load_payload("valid_payload.json")
        serializer = StudentOnboardingSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_guardian_consent_is_rejected(self):
        data = load_payload("invalid_payload_no_consent.json")
        serializer = StudentOnboardingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("guardian_consent_given", serializer.errors)

    def test_schema_mismatch_payload_is_rejected_on_every_bad_field(self):
        data = load_payload("invalid_payload_schema_mismatch.json")
        serializer = StudentOnboardingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # Exact scenario from the brief: an invalid enum value and a
        # malformed email must BOTH be caught, not just the first one.
        # Note: DRF only runs object-level validate() (the diagnosis_type
        # cross-field rule) once every per-field check passes, so a payload
        # that already fails per-field validation won't also surface the
        # diagnosis_type error in the same response — that rule is verified
        # independently below.
        self.assertIn("preferred_session_frequency", serializer.errors)
        self.assertIn("contact_email", serializer.errors)

    def test_diagnosis_type_required_when_difficulty_flagged(self):
        data = load_payload("valid_payload.json")
        data["diagnosis_type"] = ""  # strip it while flag stays true
        serializer = StudentOnboardingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("diagnosis_type", serializer.errors)

    def test_diagnosis_type_must_be_absent_when_no_difficulty(self):
        data = load_payload("valid_payload.json")
        data["has_diagnosed_learning_difficulty"] = False
        # diagnosis_type ("Dyslexia") is left populated - inconsistent state
        serializer = StudentOnboardingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("diagnosis_type", serializer.errors)
