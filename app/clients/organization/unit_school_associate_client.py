# app/clients/unit_school_associate_client.py
from typing import List
import httpx
from app.configuration.settings import settings
from app.domain.dtos.organization.unit_school_associate_dto import (
    UnitSchoolAssociateDTO
)

base_url = settings.DNED_ORGANIZATION


class UnitSchoolAssociateClient:

    _client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(
            max_connections=10,
            max_keepalive_connections=5
        )
    )

    @staticmethod
    async def fetch_associations(
        start: int = 0, limit: int = 100
    ) -> List[UnitSchoolAssociateDTO]:
        url = (
            f"{base_url}/unit_school_associates"
            f"?start={start}&limit={limit}"
        )
        response = await UnitSchoolAssociateClient._client.get(
            url, follow_redirects=True
        )
        response.raise_for_status()
        data = response.json()
        return [UnitSchoolAssociateDTO(**assoc) for assoc in data]

    @staticmethod
    async def fetch_association_by_id(
        cod_unit: str, cod_school: str, cod_period: str
    ) -> UnitSchoolAssociateDTO:
        url = (
            f"{base_url}/unit_school_associates"
            f"/{cod_unit}/{cod_school}/{cod_period}"
        )
        response = await UnitSchoolAssociateClient._client.get(url)
        response.raise_for_status()
        data = response.json()
        return UnitSchoolAssociateDTO(**data)

    @staticmethod
    async def fetch_associations_by_school(
        cod_school: str,
        period: str,
    ) -> List[UnitSchoolAssociateDTO]:
        url = (
            f"{base_url}/unit_school_associates/"
            f"by-school/{cod_school}/{period}"
        )
        response = await UnitSchoolAssociateClient._client.get(
            url, follow_redirects=True
        )
        response.raise_for_status()
        data = response.json()
        return [UnitSchoolAssociateDTO(**assoc) for assoc in data]