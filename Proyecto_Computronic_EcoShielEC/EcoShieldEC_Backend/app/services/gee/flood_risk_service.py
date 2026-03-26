from datetime import datetime
from app.models.alert_models import LocationModel, SatelliteModel, EnvironmentalFeatures, AnalysisModel, AlertResponseModel
from app.services.gee.geometry_service import GeometryService
from app.services.gee.collection_service import CollectionService
from app.services.gee.ndvi_service import NDVIService
from app.services.gee.ndwi_service import NDWIService
from app.services.gee.dem_service import DEMService

class FloodRiskService:
    def __init__(self, geometry_service: GeometryService, collection_service: CollectionService, 
                 ndvi_service: NDVIService, ndwi_service: NDWIService, dem_service: DEMService):
        self.geometry_service = geometry_service
        self.collection_service = collection_service
        self.ndvi_service = ndvi_service
        self.ndwi_service = ndwi_service
        self.dem_service = dem_service

    def get_environmental_features(self, sentinel_image, dem_image, point) -> EnvironmentalFeatures:
        ndvi_layer = self.ndvi_service.generate_layer(sentinel_image)
        ndwi_layer = self.ndwi_service.generate_layer(sentinel_image)

        ndvi_value = self.ndvi_service.get_ndvi_value_at_point(ndvi_layer, point)
        ndwi_value = self.ndwi_service.get_ndwi_value_at_point(ndwi_layer, point)
        elevation_value = self.dem_service.get_elevation_value_at_point(dem_image, point)

        return EnvironmentalFeatures(
            ndvi=ndvi_value if ndvi_value is not None else 0.0,
            ndwi=ndwi_value if ndwi_value is not None else 0.0,
            elevation=elevation_value if elevation_value is not None else 0.0,
        )

    def build_analysis(self, features: EnvironmentalFeatures) -> AnalysisModel:
        score = 0
        reasons = []

        if features.elevation < 5:
            score += 1
            reasons.append("low elevation")

        if features.ndwi > 0.2:
            score += 1
            reasons.append("high water presence")

        if features.ndvi < 0.5:
            score += 1
            reasons.append("low vegetation protection")

        if score <= 1:
            risk_level = "LOW"
            recommended_action = "Continue monitoring the area periodically."
        elif score == 2:
            risk_level = "MEDIUM"
            recommended_action = "Review the area and consider preventive mitigation actions."
        else:
            risk_level = "HIGH"
            recommended_action = "Prioritize field inspection and flood preparedness planning."

        if reasons:
            message = f"The point shows {', '.join(reasons)}."
        else:
            message = "No significant flood risk indicators were detected at this point."

        return AnalysisModel(
            overallRiskLevel=risk_level,
            riskScore=score,
            message=message,
            recommendedAction=recommended_action,
        )

    def analyze_location(self, zone: str,lat: float, lng: float, start_date: str, end_date: str,
        cloud_cover_percentage: float = 20,
    ) -> AlertResponseModel:
        point = self.geometry_service.create_point(lng, lat)
        region = self.geometry_service.create_buffered_point(lat=lat, lng=lng, buffer_meters=20000)

        sentinel_image = self.collection_service.get_median_image(
            region=region,
            start_date=start_date,
            end_date=end_date,
            cloud_cover_percentage=cloud_cover_percentage,
        )

        dem_image = self.collection_service.get_collection_elevation(region=region)

        features = self.get_environmental_features(
            sentinel_image=sentinel_image,
            dem_image=dem_image,
            point=point,
        )

        analysis = self.build_analysis(features)

        satellite_data = SatelliteModel(
            source="Sentinel-2 / Earth Engine",
            cloudCoverPercentage=cloud_cover_percentage,
            mangroveHealthNdvi=features.ndvi,
            status="processed",
        )

        location = LocationModel(
            zone=zone,
            lat=lat,
            lng=lng,
        )

        return AlertResponseModel(
            alertId=f"alert-{zone.lower().replace(' ', '-')}-{int(datetime.now().timestamp())}",
            timestamp=datetime.now(),
            location=location,
            satelliteData=satellite_data,
            iotSensorData=None,
            analysis=analysis,
        )