# app/controllers/export_controller.py
from fastapi import APIRouter, HTTPException
from app.service.use_cases.get_list_organization import ExportEmailListsService

router = APIRouter(prefix="/exports", tags=["Exports"])


@router.post("/headquarters/{cod_headquarters}/{cod_period}")
async def export_for_headquarters(cod_headquarters: str, cod_period: str):
    try:
        service = ExportEmailListsService(out_dir="exports")
        await service.generate_for_headquarters(cod_headquarters, cod_period)
        return {
            "detail": "Export completed",
            "headquarters": cod_headquarters,
            "period": cod_period
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
