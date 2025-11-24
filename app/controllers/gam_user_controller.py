from fastapi import APIRouter, HTTPException
from app.service.gam.gam_user_service import GamUserService


router = APIRouter(prefix="/gam-user", tags=["GAM"])


@router.post("/create-user/{email}")
async def create_gam_user(email: str):
    try:
        result = GamUserService.crear_usuario(email)
        return {
            "detail": f"User creation attempted for {email}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user-info/{email}")
async def get_gam_user_info(email: str):
    try:
        result = GamUserService.get_usuario_info(email)
        return {
            "detail": f"User info retrieval attempted for {email}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
