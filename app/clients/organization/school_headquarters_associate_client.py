# app/clients/school_headquarters_associate_client.py
import httpx
from app.configuration.settings import settings

base_url = settings.DNED_ORGANIZATION


class SchoolHeadquartersAssociateClient:

    @staticmethod
    async def fetch_associations(start: int = 0, limit: int = 100) -> list:
        """
        Obtiene la lista de asociaciones entre escuelas y headquarters
        con paginación.
        """
        url = (
            f"http://{base_url}/school_headquarters_associates"
            f"?start={start}&limit={limit}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def fetch_association_by_id(
        cod_school: str,
        cod_headquarters: str,
        cod_period: str,
    ) -> dict:
        """Obtiene una asociación específica entre una escuela y un
        headquarters y un periodo."""
        url = (
            f"http://{base_url}/school_headquarters_associates/"
            f"{cod_school}/{cod_headquarters}/{cod_period}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
