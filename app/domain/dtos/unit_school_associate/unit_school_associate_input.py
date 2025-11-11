from pydantic import BaseModel


class UnitSchoolAssociateInput(BaseModel):
    cod_unit: str
    cod_school: str
    cod_period: str
