from app.models.alert_models import AlertResponseModel, AnalysisModel
from app.repositories.alert_repository import AlertRepository
from app.services.analysis_service import AnalysisService # Importamos el cerebro

class MangroveService:
    def __init__(self):
        self.repository = AlertRepository()
        self.analysis = AnalysisService() # Instanciamos el análisis

    def create_new_alert(self, alert_data: AlertResponseModel):
        # 1. Extraemos los datos para el análisis
        ndvi = alert_data.satelliteData.mangroveHealthNdvi
        water = alert_data.iotSensorData.waterLevelCm

        # 2. CALCULAMOS EL RIESGO REAL
        risk_result = self.analysis.calculate_risk(ndvi, water)

        # 3. Actualizamos el objeto con el análisis real (sobrescribimos lo que envió el cliente)
        alert_data.analysis = AnalysisModel(**risk_result)

        # 4. Guardamos en DB
        document = alert_data.model_dump()
        result = self.repository.create(document)

        return {
            "message": "Alerta analizada y guardada",
            "id": str(result.inserted_id),
            "analysis_summary": risk_result
        }

    def get_current_status(self):
        # Le pide el dato al repositorio
        data = self.repository.get_latest()

        if data:
            return AlertResponseModel(**data)
        return None
