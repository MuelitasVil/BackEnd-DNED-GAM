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
        return {"detail": f"User creation attempted for {email}", "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
