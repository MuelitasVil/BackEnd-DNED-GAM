from fastapi import APIRouter
import app.clients.organization.test as organization_test_client

router = APIRouter(prefix="/test-clients", tags=["Testing Clients"])


@router.get("/")
async def test_organization_ms():
    result = await organization_test_client.UserOrganizationClient.fetch_test()
    return result
