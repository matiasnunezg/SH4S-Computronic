from app.database.mongo_connection import alerts_collection

# Obtener última alerta (orden descendente por ID)
def get_latest_alert():
    return alerts_collection.find_one(sort=[("_id", -1)])

# Crear nueva alerta
def insert_alert(alert_dict: dict):
    result = alerts_collection.insert_one(alert_dict)
    return str(result.inserted_id)
