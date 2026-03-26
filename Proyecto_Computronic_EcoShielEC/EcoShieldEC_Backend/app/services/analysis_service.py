# Función pura → fácil de testear 🔥
def calculate_risk(ndvi: float, water_level: float) -> dict:
    score = 0
    messages = []
    action = "Monitoreo constante"

    # --- NDVI ---
    if ndvi < 0 or ndvi > 1:
        raise ValueError("NDVI fuera de rango válido (0 - 1)")

    if ndvi < 0.3:
        score += 60
        messages.append("Deforestación detectada")
    elif ndvi < 0.6:
        score += 20
        messages.append("Salud del manglar estable")
    else:
        messages.append("Manglar saludable")

    # --- Nivel de agua ---
    if water_level < 0:
        raise ValueError("Nivel de agua inválido")

    if water_level > 150:
        score += 40
        messages.append("Alerta de inundación")
        action = "Evacuar y asegurar sensores"
    elif water_level < 20:
        score += 20
        messages.append("Nivel de agua bajo")
        action = "Revisar flujo de canales"

    # --- Nivel final ---
    if score >= 80:
        level = "CRITICAL"
    elif score >= 50:
        level = "WARNING"
    else:
        level = "NORMAL"

    return {
        "overallRiskLevel": level,
        "riskScore": min(score, 100),
        "message": " + ".join(messages),
        "recommendedAction": action
    }
