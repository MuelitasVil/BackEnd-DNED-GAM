from pydantic import BaseModel


class UserUnitAssociateInput(BaseModel):
    email_unal: str
    cod_unit: str
    cod_period: str
