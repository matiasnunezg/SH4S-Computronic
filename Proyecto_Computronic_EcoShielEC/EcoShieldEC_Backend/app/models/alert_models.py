from sqlite3.dbapi2 import Timestamp

from pydantic import BaseModel

class LocationModel(BaseModel):
    zone: str
    lat: float
    lng: float

class SatelliteModel(BaseModel):
    source: str
    cloudCoverPercentage: float
    mangroveHealthNdvi: float
    status: str

class IoTSensorModel(BaseModel):
    sensorId: str
    waterLevelCm: float
    isOnline: bool
    status: str

class AnalysisModel(BaseModel):
    overallRiskLevel: str
    riskScore: int
    message: str
    recommendedAction: str

#Metodo principal que agrupa todo
class AlertResponseModel(BaseModel):
    alertId: str
    timestamp: str
    location: LocationModel
    satelliteData: SatelliteModel
    iotSensorData: IoTSensorModel
    analysis: AnalysisModel
