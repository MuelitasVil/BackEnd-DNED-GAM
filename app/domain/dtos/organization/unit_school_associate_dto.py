from pydantic import BaseModel


class UnitSchoolAssociateDTO(BaseModel):
    cod_unit: str
    cod_school: str
    cod_period: str
