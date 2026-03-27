import typer
import random
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

# Colores en consola
from rich import print

# GEE
import ee
from app.services.gee.gee_initializer import GEEInitializer
from app.services.gee.geometry_service import GeometryService
from app.services.gee.collection_service import CollectionService
from app.services.gee.ndvi_service import NDVIService

#OpenAI API
from app.services.openai.openai_service import OpenAIService

# Modelos y lógica existente
from app.models.alert_models import (
    AlertResponseModel,
    LocationModel,
    SatelliteModel,
    IoTSensorModel,
    AnalysisModel
)
from app.services.analysis_service import calculate_risk
from app.repositories.alert_repository import insert_alert

app = typer.Typer()

# System Prompt
syst_msj = """
You are an environmental risk recommendation assistant for mangrove and flood monitoring scenarios.

Generate only one concise final recommendation based on:
- overallRiskLevel
- riskScore
- message
- recommendedAction

Rules:
- Maximum 2 sentences.
- Output only the recommendation.
- Be clear, short, and actionable.
- Adapt the recommendation to the severity level:
  - CRITICAL = urgent action
  - WARNING = preventive action
  - NORMAL = routine monitoring
- Use recommendedAction as fallback if needed.
- Do not explain, justify, or restate the data.
- Do not use labels, headings, bullets, or variable names.

Now generate the recommendation.

"""

# 🔥 Inicializar GEE
GEEInitializer.initialize()

# Inicializar OpenAI API
client = OpenAIService(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("BASE_URL"), system_prompt=syst_msj)


@app.command()
def populate():
    """
    Crear un snapshot de monitoreo de manglar con datos reales (NDVI) + simulados (IoT)
    """

    try:
        
        # -----------------------------
        # INPUT USUARIO
        # -----------------------------
        zone = typer.prompt("🌍 Nombre de la zona")
        lat = float(typer.prompt("📍 Latitud"))
        lng = float(typer.prompt("📍 Longitud"))

        print(f"\n[cyan]Procesando zona: {zone}...[/cyan]")

        # -----------------------------
        # GEE → NDVI REAL
        # -----------------------------
        geometry_service = GeometryService()
        ndvi_service = NDVIService()

        # ⚠️ IMPORTANTE: usamos Sentinel-2 directamente aquí
        collection_service = CollectionService("COPERNICUS/S2_SR_HARMONIZED")

        point = geometry_service.create_point(lng, lat)
        region = geometry_service.create_buffered_point(lng, lat, 500)

        collection = collection_service.get_collection(
            region=region,
            start_date="2023-01-01",
            end_date=datetime.now().strftime("%Y-%m-%d"),
            cloud_percentage=20
        )

        # 🔥 FIX (sin tocar tu service)
        image = CollectionService.get_median_image(collection)

        ndvi_layer = ndvi_service.generate_layer(image)
        ndvi_value = ndvi_service.get_ndvi_value_at_point(ndvi_layer, point)

        if ndvi_value is None:
            ndvi_value = 0.0

        print(f"[green]NDVI obtenido:[/green] {ndvi_value:.3f}")

        # -----------------------------
        # SIMULACIÓN IoT (REALISTA)
        # -----------------------------
        water_level = random.uniform(120, 450)
        is_online = random.choice([True, True, True, False])  # 75% online

        sensor_status = "OK" if is_online else "OFFLINE"

        print(f"[blue]Nivel de agua:[/blue] {water_level:.2f} cm")
        print(f"[blue]Sensor estado:[/blue] {sensor_status}")

        # -----------------------------
        # ANÁLISIS DE RIESGO
        # -----------------------------
        risk = calculate_risk(ndvi_value, water_level)
        risk.pop("recommendedAction", None)
        new_recomendation =client.get_response(str(risk))
        

        print(f"[magenta]Riesgo:[/magenta] {risk['overallRiskLevel']} ({risk['riskScore']})")

        # -----------------------------
        # CONSTRUIR MODELO (IMPORTANTE)
        # -----------------------------
        alert = AlertResponseModel(
            alertId=f"alert-{zone.lower().replace(' ', '-')}-{int(datetime.now().timestamp())}",
            timestamp=datetime.now(timezone.utc).isoformat(),

            location=LocationModel(
                zone=zone,
                lat=lat,
                lng=lng
            ),

            satelliteData=SatelliteModel(
                source="Sentinel-2",
                cloudCoverPercentage=20,
                mangroveHealthNdvi=ndvi_value,
                status="Active"
            ),

            iotSensorData=IoTSensorModel(
                sensorId=f"NODE-{random.randint(1, 99)}",
                waterLevelCm=water_level,
                isOnline=is_online,
                status=sensor_status
            ),
            
            analysis = AnalysisModel(**risk, recommendedAction=new_recomendation)
            
        )

        # -----------------------------
        # INSERTAR EN MONGO
        # -----------------------------
        inserted_id = insert_alert(alert.model_dump())

        print("\n[bold green]✅ Snapshot insertado correctamente[/bold green]")
        print(f"[yellow]ID:[/yellow] {inserted_id}")

    except Exception as e:
        print(f"[bold red]❌ Error:[/bold red] {e}")


if __name__ == "__main__":
    app()
