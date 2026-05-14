import asyncio
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session

from app.configuration.database import get_session, engine
from app.domain.dtos.jobs.job_dto import (
    JobCreateRequest,
    JobResponse,
    JobStatusResponse,
    JobProgressResponse,
    JobResultResponse,
)
from app.domain.models.job_progress import JobProgress
from app.domain.models.job_result import JobResult
from app.repository.job_repository import JobRepository
from app.repository.job_progress_repository import JobProgressRepository
from app.repository.job_result_repository import JobResultRepository
from app.service.jobs.job_service import JobService
from app.service.use_cases.update_units_of_headquaters import (
    update_units_of_headquarters,
)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def _build_job_response(job) -> JobResponse:
    status = (
        job.status.value
        if hasattr(job.status, "value")
        else job.status
    )

    return JobResponse(
        id=job.id,
        process_type=job.process_type,
        status=status,
        params=job.params,
        requested_by=job.requested_by,
        origin=job.origin,
        priority=job.priority,
        created_at=job.created_at,
        updated_at=job.updated_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
    )


def _run_job_in_background(job_id: str, payload: JobCreateRequest) -> None:
    from sqlmodel import Session

    with Session(engine) as session:
        JobService.mark_running(session, job_id)

    try:
        if payload.process_type == "update_units_by_headquarters":
            name = payload.params.get("name_headquarters")
            period = payload.params.get("period")
            if not name or not period:
                raise ValueError("Missing name_headquarters or period")
            result = asyncio.run(update_units_of_headquarters(name, period))

            processed_units = 0
            if isinstance(result, dict):
                processed_units = int(result.get("cant of updaated units", 0))

            progress = JobProgress(
                job_id=job_id,
                phase="completed",
                processed_units=processed_units,
                total_units=processed_units,
            )
            job_result = JobResult(
                job_id=job_id,
                success_count=processed_units,
                error_count=0,
            )

            with Session(engine) as session:
                JobService.mark_succeeded(
                    session, job_id, job_result, progress
                )
            return

        raise ValueError(f"Unsupported process_type: {payload.process_type}")

    except Exception as exc:
        progress = JobProgress(
            job_id=job_id,
            phase="failed",
            last_error=str(exc),
        )
        with Session(engine) as session:
            JobService.mark_failed(session, job_id, str(exc), progress)


@router.post("/", response_model=JobResponse)
async def create_job(
    payload: JobCreateRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    job = JobService.create_job(
        session,
        process_type=payload.process_type,
        params=payload.params,
        requested_by=payload.requested_by,
        origin=payload.origin or "organizational",
        priority=payload.priority or 0,
    )
    background_tasks.add_task(_run_job_in_background, job.id, payload)
    return _build_job_response(job)


@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    session: Session = Depends(get_session),
):
    job = JobRepository(session).get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    progress = JobProgressRepository(session).get_by_id(job_id)
    result = JobResultRepository(session).get_by_id(job_id)

    progress_response: Optional[JobProgressResponse] = None
    if progress:
        progress_response = JobProgressResponse(
            phase=progress.phase,
            total_units=progress.total_units,
            processed_units=progress.processed_units,
            total_emails=progress.total_emails,
            processed_emails=progress.processed_emails,
            last_error=progress.last_error,
        )

    result_response: Optional[JobResultResponse] = None
    if result:
        result_response = JobResultResponse(
            success_count=result.success_count,
            error_count=result.error_count,
            error_samples=result.error_samples,
            artifacts=result.artifacts,
        )

    return JobStatusResponse(
        job=_build_job_response(job),
        progress=progress_response,
        result=result_response,
    )
