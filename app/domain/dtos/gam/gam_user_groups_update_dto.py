from typing import List, Optional

from pydantic import BaseModel


class GamUserGroupsUpdateDto(BaseModel):
    add: Optional[List[str]] = None
    remove: Optional[List[str]] = None
    role: Optional[str] = None

    class Config:
        orm_mode = True
        extra = "allow"
