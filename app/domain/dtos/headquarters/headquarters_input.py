from pydantic import BaseModel
from typing import Optional


class HeadquartersInput(BaseModel):
    cod_headquarters: str
    email: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type_facultad: Optional[str] = None
