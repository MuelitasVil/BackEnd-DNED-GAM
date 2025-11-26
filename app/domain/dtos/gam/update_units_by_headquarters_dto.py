from pydantic import BaseModel


class UpdateUnitsByHeadquarters(BaseModel):
    name_headquarters: str
    period: str
