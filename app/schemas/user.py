from pydantic import BaseModel, EmailStr,field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) > 72:
            raise ValueError("Password too long (max 72 characters)")
        return value

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True