from fastapi import APIRouter, HTTPException
from app.services.mangrove_service import get_current_status, create_new_alert
from app.models.alert_models import AlertResponseModel

router = APIRouter()

@router.get("/manglares/status", response_model=AlertResponseModel)
def mangrove_status():
    data = get_current_status()

    if not data:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")

    return data


@router.post("/manglares/alert")
def new_alert(alert: AlertResponseModel):
    return create_new_alert(alert)
