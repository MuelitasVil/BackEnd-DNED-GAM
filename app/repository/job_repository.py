from datetime import datetime
from typing import Optional

from sqlmodel import Session

from app.domain.models.job import Job, JobStatus


class JobRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, job_id: str) -> Optional[Job]:
        return self.session.get(Job, job_id)

    def create(self, job: Job) -> Job:
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        started_at: Optional[datetime] = None,
        finished_at: Optional[datetime] = None,
    ) -> Optional[Job]:
        job = self.get_by_id(job_id)
        if not job:
            return None

        job.status = status
        job.updated_at = datetime.utcnow()
        if started_at is not None:
            job.started_at = started_at
        if finished_at is not None:
            job.finished_at = finished_at

        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job
