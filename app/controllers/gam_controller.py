from fastapi import APIRouter, HTTPException
from app.service.gam import gam_service

router = APIRouter(prefix="/gam", tags=["GAM"])


@router.get("/test-connection")
async def test_gam_connection():
    try:
        result = gam_service.GamService().test_connection()
        return {"detail": "GAM connection successful", "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-user/{email}")
async def create_gam_user(email: str):
    try:
        result = gam_service.GamService.crear_usuario(email)
        return {
            "detail": f"User creation attempted for {email}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user-info/{email}")
async def get_gam_user_info(email: str):
    try:
        result = gam_service.GamService().get_usuario_info(email)
        return {
            "detail": f"User info retrieval attempted for {email}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-group/{group_email}")
async def create_gam_group(group_email: str):
    try:
        result = gam_service.GamService().create_group(group_email)
        return {
            "detail": f"Group creation attempted for {group_email}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-group/{group_email}")
async def delete_gam_group(group_email: str):
    try:
        result = gam_service.GamService().delete_group(group_email)
        return {
            "detail": f"Group deletion attempted for {group_email}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-user-to-group/")
async def add_user_to_gam_group(
    user_email: str, group_email: str, role: str
):
    try:
        result = gam_service.GamService().add_user_to_group(
            user_email, group_email, role
        )
        return {
            "detail": "Add user {} to group {} attempted".format(
                user_email, group_email
            ),
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
