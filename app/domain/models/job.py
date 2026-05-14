from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import JSON
from sqlmodel import Field, SQLModel


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    canceled = "canceled"
    retrying = "retrying"


class Job(SQLModel, table=True):
    __tablename__ = "job"

    id: str = Field(primary_key=True, max_length=36)
    process_type: str = Field(max_length=64)
    status: JobStatus = Field(default=JobStatus.queued)
    params: Dict[str, Any] = Field(sa_column=Column(JSON), default_factory=dict)
    requested_by: Optional[str] = Field(default=None, max_length=128)
    origin: str = Field(default="organizational", max_length=64)
    priority: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
