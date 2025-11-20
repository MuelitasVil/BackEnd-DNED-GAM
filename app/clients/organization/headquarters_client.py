# app/clients/headquarters_client.py
import httpx
from fastapi import HTTPException
from app.configuration.settings import settings
from app.domain.dtos.organization.headquarters_dto import HeadquartersDTO
from app.domain.dtos.organization.email_dto import EmailDTO
from typing import List

base_url = settings.DNED_ORGANIZATION


class HeadquartersClient:

    @staticmethod
    async def fetch_headquarters(
        start: int = 0, limit: int = 100
    ) -> List[HeadquartersDTO]:
        """Obtiene la lista de todos los headquarters con paginación."""
        full_url = (
            f"{base_url}/headquarters?"
            f"start={start}&limit={limit}"
        )
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(full_url)
                response.raise_for_status()
                data = response.json()
                return [HeadquartersDTO(**hq) for hq in data]
        except httpx.HTTPStatusError as e:
            # Se lanza un HTTPException con el código de error y mensaje
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching headquarters: {e}"
            )
        except httpx.RequestError as e:
            # Captura errores de la solicitud (e.g., timeout, no conexión)
            raise HTTPException(status_code=500, detail=f"Request error: {e}")

    @staticmethod
    async def fetch_headquarter_by_id(
        cod_headquarters: str
    ) -> HeadquartersDTO:
        """Obtiene un headquarter específico por su código."""
        full_url = f"{base_url}/headquarters/{cod_headquarters}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(full_url)
                response.raise_for_status()
                data = response.json()
                return HeadquartersDTO(**data)
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching headquarter: {e}"
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {e}")

    @staticmethod
    async def fetch_email_list_of_headquarters(
        cod_headquarters: str, cod_period: str
    ) -> List[EmailDTO]:
        url = (
            f"{base_url}/headquarters/get-email-list/"
            f"{cod_headquarters}/{cod_period}"
        )
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                print(data)
                return [EmailDTO(
                    email=email[0], role=email[1]
                ) for email in data]
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching email list for headquarter: {e}"
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {e}")
