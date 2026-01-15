# app/clients/organization_client.py
import httpx
from app.configuration.settings import settings
from app.domain.dtos.organization.users_dto import (
    UserUnalDto as User
)
from typing import List
base_url = settings.DNED_ORGANIZATION


class UserOrganizationClient:

    _client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(
            max_connections=10,
            max_keepalive_connections=5
        )
    )

    @staticmethod
    async def fetch_users() -> List[User]:
        url = f"{base_url}/users_unal/"
        async with UserOrganizationClient._client as client:
            response = await client.get(url)
            response.raise_for_status()
            return [User(**user) for user in await response.json()]

    @staticmethod
    async def fetch_user_by_email(email_unal: str) -> User:
        url = f"{base_url}/users_unal/{email_unal}"
        async with UserOrganizationClient._client as client:
            response = await client.get(url)
            response.raise_for_status()
            return User(**response.json())
