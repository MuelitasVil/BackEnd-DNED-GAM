from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import JSON
from sqlmodel import Field, SQLModel


class JobResult(SQLModel, table=True):
    __tablename__ = "job_result"

    job_id: str = Field(primary_key=True, foreign_key="job.id")
    success_count: int = Field(default=0)
    error_count: int = Field(default=0)
    error_samples: Optional[Dict[str, Any]] = Field(
        sa_column=Column(JSON), default=None
    )
    artifacts: Optional[Dict[str, Any]] = Field(
        sa_column=Column(JSON), default=None
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
