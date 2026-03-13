from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Base schema with shared configuration.
    """

    model_config = ConfigDict(
        extra="ignore",  # ignore unknown fields
        from_attributes=True,  # allow ORM objects
        populate_by_name=True,
    )


class SuccessSchema(BaseModel):
    message: str
    is_success: bool = True


class ErrorSchema(BaseModel):
    error: str
    is_success: bool = True


class PaginationOutputSchema(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool
