from pydantic import BaseModel
from typing import Optional


class TypeUserInput(BaseModel):
    type_user_id: str
    name: Optional[str] = None
    description: Optional[str] = None
