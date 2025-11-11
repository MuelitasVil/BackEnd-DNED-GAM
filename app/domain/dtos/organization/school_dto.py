from typing import Optional
from pydantic import BaseModel


class SchoolDTO(BaseModel):
    cod_school: str
    email: Optional[str]
    name: Optional[str]
    description: Optional[str]
    type_facultad: Optional[str]
