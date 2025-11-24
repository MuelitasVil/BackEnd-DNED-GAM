# app/controllers/export_controller.py
from fastapi import APIRouter, HTTPException
from app.service.use_cases.get_list_organization_v2 import (
    generate_for_headquarters
)

router = APIRouter(prefix="/exports", tags=["Exports"])


@router.post("/headquarters/{cod_headquarters}/{cod_period}")
async def export_for_headquarters(cod_headquarters: str, cod_period: str):
    try:
        result = await generate_for_headquarters(
            cod_headquarters, cod_period
        )
        return {
            "detail": f"Export attempted for headquarters {cod_headquarters}"
            f" and period {cod_period}",
            "output": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
