from typing import Optional

from pydantic import BaseModel


class GamUserSuspendDto(BaseModel):
    suspend: Optional[bool] = None

    class Config:
        orm_mode = True
        extra = "allow"
