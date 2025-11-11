# app/clients/unit_school_associate_client.py
import httpx
from app.configuration.settings import settings

base_url = settings.DNED_ORGANIZATION


class UnitSchoolAssociateClient:

    @staticmethod
    async def fetch_associations(start: int = 0, limit: int = 100) -> list:
        """Obtiene la lista de todas las asociaciones entre unidades
        y escuelas con paginación."""
        url = (
            f"http://{base_url}/unit_school_associates"
            f"?start={start}&limit={limit}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def fetch_association_by_id(
        cod_unit: str, cod_school: str, cod_period: str
    ) -> dict:
        """Obtiene una asociación específica entre una unidad,
        una escuela y un periodo."""
        url = (
            f"http://{base_url}/unit_school_associates"
            f"/{cod_unit}/{cod_school}/{cod_period}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
