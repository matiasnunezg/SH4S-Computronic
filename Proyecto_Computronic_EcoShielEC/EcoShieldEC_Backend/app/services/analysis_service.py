class AnalysisService:
    def calculate_risk(self, ndvi: float, water_level: float):
        score = 0
        message = ""
        action = ""

        # Lógica para NDVI (Satélite - Doménica)
        if ndvi < 0.3:
            score += 60  # Riesgo alto por deforestación
            message = "Deforestación detectada"
        elif ndvi < 0.6:
            score += 20
            message = "Salud del manglar estable"
        else:
            message = "Manglar saludable"

        # Lógica para Nivel de Agua (IoT - Aarón)
        # Supongamos que > 150cm es inundación peligrosa
        if water_level > 150:
            score += 40
            message += " + Alerta de inundación"
            action = "Evacuar y asegurar sensores"
        elif water_level < 20:
            score += 20
            message += " + Nivel de agua bajo"
            action = "Revisar flujo de canales"
        else:
            action = "Monitoreo constante"

        # Determinación del nivel final
        if score >= 80:
            level = "CRITICAL"
        elif score >= 50:
            level = "WARNING"
        else:
            level = "NORMAL"

        return {
            "overallRiskLevel": level,
            "riskScore": min(score, 100), # Que no pase de 100
            "message": message,
            "recommendedAction": action
        }
