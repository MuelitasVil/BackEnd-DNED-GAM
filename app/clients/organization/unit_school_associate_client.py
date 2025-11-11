# app/clients/unit_school_associate_client.py
from ast import List
import httpx
from app.configuration.settings import settings
from app.domain.dtos.organization.unit_school_associate_dto import (
    UnitSchoolAssociateDTO as usa
)

base_url = settings.DNED_ORGANIZATION


class UnitSchoolAssociateClient:

    @staticmethod
    async def fetch_associations(
        start: int = 0, limit: int = 100
    ) -> List[usa]:
        url = (
            f"http://{base_url}/unit_school_associates"
            f"?start={start}&limit={limit}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [usa(**assoc) for assoc in data]

    @staticmethod
    async def fetch_association_by_id(
        cod_unit: str, cod_school: str, cod_period: str
    ) -> usa:
        url = (
            f"http://{base_url}/unit_school_associates"
            f"/{cod_unit}/{cod_school}/{cod_period}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return usa(**data)
