from pydantic import BaseModel


class SchoolHeadquartersAssociateInput(BaseModel):
    cod_school: str
    cod_headquarters: str
    cod_period: str
