from fastapi import HTTPException
from app.models.alert_models import AlertResponseModel, AnalysisModel
from app.repositories.alert_repository import get_latest_alert, insert_alert
from app.services.analysis_service import calculate_risk


def create_new_alert(alert_data: AlertResponseModel):
    try:
        # Extraer datos críticos
        ndvi = alert_data.satelliteData.mangroveHealthNdvi
        water = alert_data.iotSensorData.waterLevelCm

        # Calcular riesgo real
        risk_result = calculate_risk(ndvi, water)

        # Sobrescribir análisis del cliente (seguridad 🔥)
        alert_data.analysis = AnalysisModel(**risk_result)

        # Guardar en DB
        document = alert_data.model_dump()
        inserted_id = insert_alert(document)

        return {
            "message": "Alerta analizada y guardada correctamente",
            "id": inserted_id,
            "analysis_summary": risk_result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_current_status():
    data = get_latest_alert()

    if not data:
        return None

    # Convertir ObjectId a string
    data["_id"] = str(data["_id"])

    return AlertResponseModel(**data)
