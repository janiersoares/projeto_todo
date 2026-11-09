from pydantic import BaseModel, EmailStr, Field, field_validator


def normalize_email(value: str) -> str:
    return value.strip().lower()


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("email")
    @classmethod
    def normalize(cls, value):
        return normalize_email(value)


class UserOut(BaseModel):
    id: int
    email: str
    created_at: str

    @classmethod
    def from_model(cls, user):
        return cls(
            id=user["id"],
            email=user["email"],
            created_at=user["created_at"].isoformat(),
        )


class LoginBody(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize(cls, value):
        return normalize_email(value)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"