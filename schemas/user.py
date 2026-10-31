from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return value.strip().lower()


class UserOut(BaseModel):
    id: int
    email: str
    created_at: str


class LoginBody(BaseModel):
    email: EmailStr
    password: str