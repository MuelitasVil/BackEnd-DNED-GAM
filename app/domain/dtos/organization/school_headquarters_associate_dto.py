from pydantic import BaseModel


class SchoolHeadquartersAssociateDTO(BaseModel):
    cod_school: str
    cod_headquarters: str
    cod_period: str
