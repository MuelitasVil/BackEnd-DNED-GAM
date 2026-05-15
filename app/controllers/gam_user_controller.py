from fastapi import APIRouter, HTTPException, Body, Query
from app.service.gam import gam_user_service as GamService
from app.domain.dtos.gam import (
    GamUserDto,
    GamUserQuotaDto,
    GamUserUpdateDto,
    GamUserOuUpdateDto,
    GamUserGroupsUpdateDto,
    GamUserLicensesUpdateDto,
    GamUserSuspendDto,
)


router = APIRouter(prefix="/gam-user", tags=["GAM-User"])


@router.get("/{email}", response_model=GamUserDto)
async def get_gam_user(email: str, quick: bool = Query(False)):
    try:
        dto = GamService.info_user(email, quick=quick)
        return dto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{email}", response_model=GamUserDto)
async def patch_gam_user(
    email: str,
    payload: GamUserUpdateDto = Body(...),
    preview: bool = Query(False)
):
    try:
        result = GamService.update_user_json(
            email,
            payload,
            preview=preview
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{email}/ou", response_model=GamUserDto)
async def patch_gam_user_ou(
    email: str,
    payload: GamUserOuUpdateDto = Body(...),
    preview: bool = Query(False)
):
    try:
        result = GamService.move_user_ou(
            email,
            payload.org_unit,
            immutableous=payload.immutableous,
            preview=preview,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{email}/groups", response_model=GamUserDto)
async def patch_gam_user_groups(
    email: str,
    payload: GamUserGroupsUpdateDto = Body(...)
):
    try:
        result = GamService.update_user_groups(
            email,
            add=payload.add or [],
            remove=payload.remove or [],
            role=payload.role,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{email}/licenses", response_model=GamUserDto)
async def post_gam_user_licenses(
    email: str,
    payload: GamUserLicensesUpdateDto = Body(...)
):
    try:
        result = GamService.manage_licenses(
            email,
            add=payload.add or [],
            remove=payload.remove or [],
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{email}/quota", response_model=GamUserQuotaDto)
async def post_gam_user_quota(email: str):
    try:
        result = GamService.get_drive_quota(email)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{email}/suspend", response_model=GamUserDto)
async def post_gam_user_suspend(
    email: str,
    payload: GamUserSuspendDto = Body(...)
):
    try:
        suspend = True if payload.suspend is None else payload.suspend
        result = GamService.suspend_user(email, suspend=suspend)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{email}/activate", response_model=GamUserDto)
async def post_gam_user_activate(
    email: str,
    payload: GamUserSuspendDto = Body(default_factory=GamUserSuspendDto)
):
    try:
        suspend = False if payload.suspend is None else payload.suspend
        result = GamService.suspend_user(email, suspend=suspend)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
