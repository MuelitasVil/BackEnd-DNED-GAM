# app/clients/school_client.py
import httpx
from app.configuration.settings import settings
from app.domain.dtos.organization.school_dto import SchoolDTO
from app.domain.dtos.organization.email_dto import EmailDTO
from typing import List

base_url = settings.DNED_ORGANIZATION


class SchoolClient:
    _client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(
            max_connections=10,
            max_keepalive_connections=5
        )
    )

    @staticmethod
    async def fetch_schools(
        start: int = 0, limit: int = 100
    ) -> List[SchoolDTO]:
        url = f"{base_url}/schools?start={start}&limit={limit}"
        response = await SchoolClient._client.get(url)
        response.raise_for_status()
        data = await response.json()
        return [SchoolDTO(**school) for school in data]

    @staticmethod
    async def fetch_school_by_id(cod_school: str) -> SchoolDTO:
        url = f"{base_url}/schools/{cod_school}"
        response = await SchoolClient._client.get(url)
        response.raise_for_status()
        data = await response.json()
        return SchoolDTO(**data)

    @staticmethod
    async def fetch_email_list_of_school(
        cod_school: str,
        cod_period: str
    ) -> List[EmailDTO]:
        url = (
            f"{base_url}/schools/get-email-list/"
            f"{cod_school}/{cod_period}"
        )
        response = await SchoolClient._client.get(url)
        response.raise_for_status()
        data = await response.json()
        return [EmailDTO(
                    email=email[0], role=email[1]
                    ) for email in data]
