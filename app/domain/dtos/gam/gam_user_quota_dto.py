from typing import Any, Dict, Optional

from pydantic import BaseModel


class GamUserQuotaDto(BaseModel):
    drive: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True
        extra = "allow"
