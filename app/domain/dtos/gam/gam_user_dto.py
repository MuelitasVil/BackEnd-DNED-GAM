from typing import List, Optional

from pydantic import BaseModel

from app.domain.dtos.gam.gam_user_group_dto import GamUserGroup
from app.domain.dtos.gam.gam_user_license_dto import GamUserLicense
from app.domain.dtos.gam.gam_user_settings_dto import GamUserSettings


class GamUserDto(BaseModel):
    username: Optional[str] = None
    settings: Optional[GamUserSettings] = None
    groups: List[GamUserGroup] = []
    licenses: List[GamUserLicense] = []
    raw_output: Optional[str] = None

    class Config:
        orm_mode = True
