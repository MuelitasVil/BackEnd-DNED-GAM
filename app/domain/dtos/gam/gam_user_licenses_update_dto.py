from typing import List, Optional

from pydantic import BaseModel


class GamUserLicensesUpdateDto(BaseModel):
    add: Optional[List[str]] = None
    remove: Optional[List[str]] = None

    class Config:
        orm_mode = True
        extra = "allow"
