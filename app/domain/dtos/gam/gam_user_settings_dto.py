from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class GamUserSettings(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    languages: Optional[str] = None
    is_super_admin: Optional[bool] = None
    is_delegated_admin: Optional[bool] = None
    two_step_enrolled: Optional[bool] = None
    two_step_enforced: Optional[bool] = None
    has_agreed_to_terms: Optional[bool] = None
    ip_whitelisted: Optional[bool] = None
    account_suspended: Optional[bool] = None
    is_archived: Optional[bool] = None
    must_change_password: Optional[bool] = None
    google_unique_id: Optional[str] = None
    customer_id: Optional[str] = None
    mailbox_is_setup: Optional[bool] = None
    included_in_gal: Optional[bool] = None
    creation_time: Optional[datetime] = None
    last_login_time: Optional[datetime] = None
    google_org_unit_path: Optional[str] = None
    recovery_email: Optional[str] = None
    photo_url: Optional[HttpUrl] = None

    class Config:
        orm_mode = True
