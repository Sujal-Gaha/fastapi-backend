from pydantic import BaseModel, model_validator


class StripLowerMixin(BaseModel):
    """Mixin to strip whitespace and lowercase specific fields."""

    @model_validator(mode="before")
    @classmethod
    def strip_and_lower(cls, values: dict) -> dict:
        # Fields that should be stripped and lowercased
        strip_lower_fields = ["email", "slug"]
        # Fields that should only be stripped
        strip_fields = ["username"]

        for field in strip_lower_fields:
            if field in values and isinstance(values[field], str):
                values[field] = values[field].strip().lower()

        for field in strip_fields:
            if field in values and isinstance(values[field], str):
                values[field] = values[field].strip()

        return values
