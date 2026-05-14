from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class JobProgress(SQLModel, table=True):
    __tablename__ = "job_progress"

    job_id: str = Field(primary_key=True, foreign_key="job.id")
    phase: str = Field(default="queued", max_length=64)
    total_units: int = Field(default=0)
    processed_units: int = Field(default=0)
    total_emails: int = Field(default=0)
    processed_emails: int = Field(default=0)
    last_error: Optional[str] = Field(default=None, max_length=512)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
