from fastapi import APIRouter
from app.services.mangrove_service import MangroveService
from app.models.alert_models import AlertResponseModel

router = APIRouter()
service = MangroveService()

@router.get("/api/v1/manglares/status", response_model=AlertResponseModel)
def get_mangrove_status():
    return service.get_current_status()

@router.post("/api/v1/manglares/alert")
def create_alert(alert: AlertResponseModel):
    return service.create_new_alert(alert)
