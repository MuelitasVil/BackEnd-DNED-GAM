from fastapi import APIRouter, HTTPException
import app.clients.organization.test as organization_test_client
from app.service.gam import gam_service

router = APIRouter(prefix="/test-clients", tags=["Testing Clients"])


@router.get("/backend-organization")
async def test_organization_ms():
    result = await organization_test_client.UserOrganizationClient.fetch_test()
    return result


@router.get("/gam-connection")
async def test_gam_connection():
    try:
        result = gam_service.GamService().test_connection()
        return {"detail": "GAM connection successful", "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
