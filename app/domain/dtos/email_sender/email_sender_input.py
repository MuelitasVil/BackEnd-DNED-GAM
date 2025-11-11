from pydantic import BaseModel, EmailStr
from typing import Optional


class EmailSenderInput(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str] = None
    org_type: str = 'GLOBAL'
    org_code: Optional[str] = None
    sede_code: Optional[str] = None
    level: str = 'ANY'
    role: str = 'OWNER'
    priority: int = 100
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
