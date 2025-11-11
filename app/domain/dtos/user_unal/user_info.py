from pydantic import BaseModel
from typing import Optional


class UserInfoAssociation(BaseModel):
    email_unal: str
    document: Optional[str] = None
    name: str
    lastname: str
    full_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    headquarters: Optional[str] = None
    period_associations: dict
