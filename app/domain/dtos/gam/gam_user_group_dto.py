from typing import Optional

from pydantic import BaseModel


class GamUserGroup(BaseModel):
    name: str
    email: Optional[str] = None

    class Config:
        orm_mode = True
