from datetime import datetime
from typing import Optional

from sqlmodel import Session

from app.domain.models.job_progress import JobProgress


class JobProgressRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, job_id: str) -> Optional[JobProgress]:
        return self.session.get(JobProgress, job_id)

    def upsert(self, progress: JobProgress) -> JobProgress:
        existing = self.get_by_id(progress.job_id)
        if existing:
            existing.phase = progress.phase
            existing.total_units = progress.total_units
            existing.processed_units = progress.processed_units
            existing.total_emails = progress.total_emails
            existing.processed_emails = progress.processed_emails
            existing.last_error = progress.last_error
            existing.updated_at = datetime.utcnow()
            self.session.add(existing)
            self.session.commit()
            self.session.refresh(existing)
            return existing

        self.session.add(progress)
        self.session.commit()
        self.session.refresh(progress)
        return progress
