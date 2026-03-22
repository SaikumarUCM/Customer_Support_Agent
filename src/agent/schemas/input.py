from pydantic import BaseModel, Field, field_validator


class UserInput(BaseModel):
    """Raw input from the API caller."""

    message: str = Field(..., min_length=1, max_length=4000, description="The user's support message")
    user_id: str = Field(..., min_length=1, max_length=128, description="Unique user identifier")
    session_id: str = Field(
        default="",
        max_length=128,
        description="Conversation session ID for multi-turn support",
    )
    locale: str = Field(default="en", max_length=10, description="BCP-47 language tag")

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("message must not be blank")
        return stripped

    @field_validator("user_id")
    @classmethod
    def user_id_no_whitespace(cls, v: str) -> str:
        if " " in v:
            raise ValueError("user_id must not contain spaces")
        return v
