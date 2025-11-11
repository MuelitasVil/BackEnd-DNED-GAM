# app/clients/organization_client.py
import httpx
from app.configuration.settings import settings

base_url = settings.DNED_ORGANIZATION


class UserOrganizationClient:

    @staticmethod
    async def fetch_test() -> dict:
        url = f"http://{base_url}/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
