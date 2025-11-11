# app/clients/organization_client.py
import httpx
from app.configuration.config import config

base_url = config.DNED_ORGANIZATION


class UserOrganizationClient:

    @staticmethod
    async def fetch_users() -> dict:
        url = f"http://{base_url}/users_unal/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def fetch_user_by_email(email_unal: str) -> dict:
        url = f"http://{base_url}/users_unal/{email_unal}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
