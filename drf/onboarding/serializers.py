from rest_framework import serializers

from .models import SessionFrequency, StudentOnboarding


class StudentOnboardingSerializer(serializers.ModelSerializer):
    """DCYN serializer: 'Deconstruct Complex [inputs into strict] Yes/No.'

    Every field that could otherwise be left to human interpretation is
    forced into an exact, bounded shape at the serializer boundary — before
    a record is ever promoted from D0 (raw landing) to D1 (staged/enforced).
    No downstream code, human or automated, has to guess what a field means.
    """

    class Meta:
        model = StudentOnboarding
        fields = [
            "record_id",
            "full_name",
            "date_of_birth",
            "has_diagnosed_learning_difficulty",
            "diagnosis_type",
            "guardian_consent_given",
            "requires_lsa_support",
            "preferred_session_frequency",
            "contact_email",
            "submitted_at",
        ]
        read_only_fields = ["record_id", "submitted_at"]

    full_name = serializers.CharField(
        max_length=120,
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "full_name is required and cannot be blank — no placeholder values accepted.",
            "max_length": "full_name must not exceed 120 characters.",
        },
    )

    # Exact enum, not free text — matches the fixed choices in the model
    # and in terraform/schemas/student_onboarding_bq_schema.json.
    preferred_session_frequency = serializers.ChoiceField(
        choices=SessionFrequency.choices,
        error_messages={
            "invalid_choice": (
                "preferred_session_frequency must be one of: "
                f"{', '.join(c[0] for c in SessionFrequency.choices)}. No other value is accepted."
            )
        },
    )

    contact_email = serializers.EmailField(required=True)

    def validate_guardian_consent_given(self, value):
        """A record without explicit guardian consent is rejected outright —
        this is not a soft warning, it is a hard validation failure. There is
        no path for this record to reach D1 without consent = True."""
        if value is not True:
            raise serializers.ValidationError(
                "guardian_consent_given must be true. Records without explicit "
                "guardian consent cannot be promoted to D1 staged/enforced."
            )
        return value

    def validate(self, attrs):
        """Object-level DCYN rule: diagnosis_type is REQUIRED when
        has_diagnosed_learning_difficulty is True, and must be absent
        otherwise. Either direction being wrong is a hard validation error —
        there is no 'best guess' branch."""
        has_diagnosis = attrs.get("has_diagnosed_learning_difficulty")
        diagnosis_type = attrs.get("diagnosis_type")

        if has_diagnosis and not diagnosis_type:
            raise serializers.ValidationError(
                {
                    "diagnosis_type": (
                        "diagnosis_type is required when "
                        "has_diagnosed_learning_difficulty is true."
                    )
                }
            )

        if not has_diagnosis and diagnosis_type:
            raise serializers.ValidationError(
                {
                    "diagnosis_type": (
                        "diagnosis_type must be empty when "
                        "has_diagnosed_learning_difficulty is false — "
                        "no inconsistent state is allowed to reach D1."
                    )
                }
            )

        return attrs
