# app/clients/headquarters_client.py
import httpx
from app.configuration.settings import settings
from app.domain.dtos.organization.headquarters_dto import HeadquartersDTO
from app.domain.dtos.organization.email_dto import EmailListDTO
from typing import List

base_url = settings.DNED_ORGANIZATION


class HeadquartersClient:

    @staticmethod
    async def fetch_headquarters(
        start: int = 0, limit: int = 100
    ) -> List[HeadquartersDTO]:
        """Obtiene la lista de todos los headquarters con paginación."""
        url = f"http://{base_url}/headquarters?start={start}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [HeadquartersDTO(**hq) for hq in data]

    @staticmethod
    async def fetch_headquarter_by_id(
        cod_headquarters: str
    ) -> HeadquartersDTO:
        """Obtiene un headquarter específico por su código."""
        url = f"http://{base_url}/headquarters/{cod_headquarters}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return HeadquartersDTO(**data)

    @staticmethod
    async def fetch_email_list_of_headquarters(
        cod_headquarters: str, cod_period: str
    ) -> List[EmailListDTO]:
        """Obtiene la lista de correos electrónicos de
        un headquarter para un periodo específico."""
        url = (
            f"http://{base_url}/get-email-list/"
            f"{cod_headquarters}/{cod_period}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [EmailListDTO(**email) for email in data]
