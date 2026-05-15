from typing import Optional

from pydantic import BaseModel


class GamUserLicense(BaseModel):
    sku_id: Optional[str] = None
    sku_name: Optional[str] = None

    class Config:
        orm_mode = True
