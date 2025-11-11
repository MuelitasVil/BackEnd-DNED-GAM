from pydantic import BaseModel, EmailStr


class RegisterInput(BaseModel):
    email: EmailStr
    password: str
