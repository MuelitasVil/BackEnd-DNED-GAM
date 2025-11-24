from fastapi import APIRouter, HTTPException
from app.service.gam.gam_group_service import GamGroupService

router = APIRouter(prefix="/gam-group", tags=["GAM"])


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
