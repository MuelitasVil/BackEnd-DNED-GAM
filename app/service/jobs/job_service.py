from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

from sqlmodel import Session

from app.domain.models.job import Job, JobStatus
from app.domain.models.job_progress import JobProgress
from app.domain.models.job_result import JobResult
from app.repository.job_repository import JobRepository
from app.repository.job_progress_repository import JobProgressRepository
from app.repository.job_result_repository import JobResultRepository


class JobService:
    @staticmethod
    def create_job(
        session: Session,
        process_type: str,
        params: Dict[str, Any],
        requested_by: Optional[str] = None,
        origin: str = "organizational",
        priority: int = 0,
    ) -> Job:
        job_id = str(uuid4())
        now = datetime.now()
        job = Job(
            id=job_id,
            process_type=process_type,
            status=JobStatus.queued,
            params=params,
            requested_by=requested_by,
            origin=origin,
            priority=priority,
            created_at=now,
            updated_at=now,
        )

        repo = JobRepository(session)
        job = repo.create(job)

        progress_repo = JobProgressRepository(session)
        progress_repo.upsert(
            JobProgress(job_id=job_id, phase="queued", updated_at=now)
        )
        return job

    @staticmethod
    def mark_running(session: Session, job_id: str) -> Optional[Job]:
        return JobRepository(session).update_status(
            job_id, JobStatus.running, started_at=datetime.now()
        )

    @staticmethod
    def mark_succeeded(
        session: Session,
        job_id: str,
        result: Optional[JobResult] = None,
        progress: Optional[JobProgress] = None,
    ) -> Optional[Job]:
        if progress:
            JobProgressRepository(session).upsert(progress)
        if result:
            JobResultRepository(session).upsert(result)
        return JobRepository(session).update_status(
            job_id, JobStatus.succeeded, finished_at=datetime.now()
        )

    @staticmethod
    def mark_failed(
        session: Session,
        job_id: str,
        error_message: str,
        progress: Optional[JobProgress] = None,
    ) -> Optional[Job]:
        if progress:
            progress.last_error = error_message
            JobProgressRepository(session).upsert(progress)
        return JobRepository(session).update_status(
            job_id, JobStatus.failed, finished_at=datetime.utcnow()
        )
