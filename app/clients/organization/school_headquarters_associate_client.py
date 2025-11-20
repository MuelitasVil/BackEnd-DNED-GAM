# app/clients/school_headquarters_associate_client.py
import httpx
from app.configuration.settings import settings
from app.domain.dtos.organization.school_headquarters_associate_dto import (
    SchoolHeadquartersAssociateDTO as sch
)
from typing import List

base_url = settings.DNED_ORGANIZATION


class SchoolHeadquartersAssociateClient:

    @staticmethod
    async def fetch_associations(
        start: int = 0, limit: int = 100
    ) -> List[sch]:
        url = (
            f"{base_url}/school_headquarters_associates"
            f"?start={start}&limit={limit}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            data = response.json()
            return [sch(**assoc) for assoc in data]

    @staticmethod
    async def fetch_association_by_id(
        cod_school: str,
        cod_headquarters: str,
        cod_period: str,
    ) -> sch:
        url = (
            f"{base_url}/school_headquarters_associates/"
            f"{cod_school}/{cod_headquarters}/{cod_period}"
        )
        print(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            return sch(**data)

    @staticmethod
    async def fetch_associations_by_headquarters(
        cod_headquarters: str,
        period: str,
    ) -> List[sch]:
        url = (
            f"{base_url}/school_headquarters_associates/"
            f"headquarters/{cod_headquarters}/{period}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            data = response.json()
            return [sch(**assoc) for assoc in data]
