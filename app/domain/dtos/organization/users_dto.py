from datetime import date
from typing import Optional
from pydantic import BaseModel


class UnitUnalDTO(BaseModel):
    email_unal: str
    document: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    gender: Optional[str]
    birth_date: Optional[date]
    headquarter: Optional[str]
