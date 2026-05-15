from typing import Optional

from pydantic import BaseModel


class GamUserOuUpdateDto(BaseModel):
    org_unit: Optional[str] = None
    immutableous: Optional[str] = None

    class Config:
        orm_mode = True
        extra = "allow"
