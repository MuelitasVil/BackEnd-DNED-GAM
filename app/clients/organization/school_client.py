# app/clients/school_client.py
import httpx
from app.configuration.settings import settings

base_url = settings.DNED_ORGANIZATION


class SchoolClient:

    @staticmethod
    async def fetch_schools(start: int = 0, limit: int = 100) -> list:
        """Obtiene la lista de todas las escuelas con paginación."""
        url = f"http://{base_url}/schools?start={start}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def fetch_school_by_id(cod_school: str) -> dict:
        """Obtiene una escuela específica por su código."""
        url = f"http://{base_url}/schools/{cod_school}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def fetch_email_list_of_school(
        cod_school: str, cod_period: str
    ) -> list:
        """Obtiene la lista de correos electrónicos de una escuela para un
        periodo específico."""
        url = f"http://{base_url}/get-email-list/{cod_school}/{cod_period}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
