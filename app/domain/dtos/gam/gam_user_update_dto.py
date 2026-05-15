from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class GamUserUpdateDto(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    recovery_email: Optional[str] = None
    thumbnail_photo_url: Optional[str] = None
    org_unit_path: Optional[str] = None
    primary_email: Optional[str] = None
    suspended: Optional[bool] = None
    archived: Optional[bool] = None
    change_password_at_next_login: Optional[bool] = None
    include_in_global_address_list: Optional[bool] = None
    languages: Optional[str] = None
    name: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="allow")

    def to_patch_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, exclude_unset=True)
