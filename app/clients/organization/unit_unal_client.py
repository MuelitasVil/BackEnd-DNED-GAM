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
    _client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=5.0,
            read=10.0,
            write=5.0,
            pool=5.0
        ),
        limits=httpx.Limits(
            max_connections=20,
            max_keepalive_connections=10
        )
    )

    @staticmethod
    async def fetch_units(
        start: int = 0, limit: int = 100
    ) -> list[UnitUnalDTO]:
        """Obtiene la lista de todas las unidades con paginación."""
        url = f"{base_url}/units_unal?start={start}&limit={limit}"
        response = await UnitUnalClient._client.get(url)
        response.raise_for_status()
        data = response.json()
        return [UnitUnalDTO(**item) for item in data]

    @staticmethod
    async def fetch_unit_by_id(cod_unit: str) -> UnitUnalDTO:
        """Obtiene una unidad específica por su código."""
        url = f"{base_url}/units_unal/{cod_unit}"
        response = await UnitUnalClient._client.get(url)
        response.raise_for_status()
        return UnitUnalDTO(**response.json())

    @staticmethod
    async def fetch_email_list_of_unit(
        cod_unit: str, period: str
    ) -> list[EmailDTO]:
        url = f"{base_url}/units_unal/get-email-list/{cod_unit}/{period}"
        response = await UnitUnalClient._client.get(url)
        response.raise_for_status()
        return [...]
