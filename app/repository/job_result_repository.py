from datetime import datetime
from typing import Optional

from sqlmodel import Session

from app.domain.models.job_result import JobResult


class JobResultRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, job_id: str) -> Optional[JobResult]:
        return self.session.get(JobResult, job_id)

    def upsert(self, result: JobResult) -> JobResult:
        existing = self.get_by_id(result.job_id)
        if existing:
            existing.success_count = result.success_count
            existing.error_count = result.error_count
            existing.error_samples = result.error_samples
            existing.artifacts = result.artifacts
            self.session.add(existing)
            self.session.commit()
            self.session.refresh(existing)
            return existing

        result.created_at = datetime.utcnow()
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result
