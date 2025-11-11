from typing import Optional
from pydantic import BaseModel


class UnitUnalDTO(BaseModel):
    cod_unit: str
    email: Optional[str]
    name: Optional[str]
    description: Optional[str]
    type_unit: Optional[str]
