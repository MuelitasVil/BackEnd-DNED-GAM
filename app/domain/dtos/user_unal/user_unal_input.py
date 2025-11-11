from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class UserUnalInput(BaseModel):
    email_unal: EmailStr
    document: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    full_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    headquarters: Optional[str] = None
