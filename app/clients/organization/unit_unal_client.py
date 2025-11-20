# app/clients/unit_unal_client.py
import httpx
from app.configuration.settings import settings
from app.domain.dtos.organization.unit_unal_dto import (
    UnitUnalDTO
)
from app.domain.dtos.organization.email_dto import (
    EmailDTO
)

base_url = settings.DNED_ORGANIZATION


class UnitUnalClient:

    @staticmethod
    async def fetch_units(
        start: int = 0, limit: int = 100
    ) -> list[UnitUnalDTO]:
        """Obtiene la lista de todas las unidades con paginación."""
        url = f"{base_url}/units_unal?start={start}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return [UnitUnalDTO(**item) for item in response.json()]

    @staticmethod
    async def fetch_unit_by_id(cod_unit: str) -> UnitUnalDTO:
        """Obtiene una unidad específica por su código."""
        url = f"{base_url}/units_unal/{cod_unit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return UnitUnalDTO(**response.json())

    @staticmethod
    async def fetch_email_list_of_unit(
        cod_unit: str, period: str
    ) -> list[EmailDTO]:
        """Obtiene la lista de correos electrónicos de una
        unidad para un periodo específico."""
        url = (
            f"{base_url}/units_unal/get-email-list/"
            f"{cod_unit}/{period}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return [EmailDTO(
                    email=email[0], role=email[1]
                    ) for email in response.json()]
