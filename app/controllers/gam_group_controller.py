from fastapi import APIRouter, HTTPException
from app.domain.dtos.gam.update_units_by_headquarters_dto import (
    UpdateUnitsByHeadquarters
)
from app.service.gam.gam_group_service import GamGroupService
from app.service.use_cases.update_units_of_headquaters import (
    update_units_of_headquarters
)

router = APIRouter(prefix="/gam-group", tags=["GAM-Group"])


@router.post("/create-group/{group_email}")
async def create_gam_group(group_email: str):
    try:
        result = GamGroupService.create_group(group_email)
        return {
            "detail": f"Group creation attempted for {group_email}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-group/{group_email}")
async def delete_gam_group(group_email: str):
    try:
        result = GamGroupService.delete_group(group_email)
        return {
            "detail": f"Group deletion attempted for {group_email}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-user-member-to-group/")
async def add_user_to_gam_group(
    user_email: str, group_email: str, role: str
):
    try:
        result = GamGroupService.add_user_member_to_group(
            user_email, group_email
        )
        return {
            "detail": "Add user {} to group {} attempted".format(
                user_email, group_email
            ),
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-user-owner-to-group/")
async def add_owner_to_gam_group(
    user_email: str, group_email: str, role: str
):
    try:
        result = GamGroupService.add_user_owener_to_group(
            user_email, group_email, role
        )
        return {
            "detail": "Add owner {} to group {} attempted".format(
                user_email, group_email
            ),
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-all-units-by-headquarters")
async def update_all_units_by_headquarters(
    data: UpdateUnitsByHeadquarters
):
    try:
        await update_units_of_headquarters(
            data.name_headquarters, data.period
        )
        return {
            "detail": f"Update of units for headquarters "
            f"{data.name_headquarters} in period {data.period} attempted"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
