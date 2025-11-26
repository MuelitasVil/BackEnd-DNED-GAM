from typing import Optional
from pydantic import BaseModel


class HeadquartersDTO(BaseModel):
    cod_headquarters: str
    email: str
    name: str
    description: Optional[str] = None
    type_facultad: str
