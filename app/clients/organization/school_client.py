# app/clients/school_client.py
import httpx
from app.configuration.settings import settings
from app.domain.dtos.organization.school_dto import SchoolDTO
from app.domain.dtos.organization.email_dto import EmailListDTO
from typing import List

base_url = settings.DNED_ORGANIZATION


class SchoolClient:

    @staticmethod
    async def fetch_schools(
        start: int = 0, limit: int = 100
    ) -> List[SchoolDTO]:
        url = f"http://{base_url}/schools?start={start}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [SchoolDTO(**school) for school in data]

    @staticmethod
    async def fetch_school_by_id(cod_school: str) -> SchoolDTO:
        url = f"http://{base_url}/schools/{cod_school}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return SchoolDTO(**data)

    @staticmethod
    async def fetch_email_list_of_school(
        cod_school: str,
        cod_period: str
    ) -> List[EmailListDTO]:
        url = f"http://{base_url}/get-email-list/{cod_school}/{cod_period}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [EmailListDTO(**email) for email in data]
