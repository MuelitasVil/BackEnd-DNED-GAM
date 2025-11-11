from pydantic import BaseModel


class HeadquartersDTO(BaseModel):
    cod_headquarters: str
    email: str
    name: str
    description: str
    type_facultad: str
