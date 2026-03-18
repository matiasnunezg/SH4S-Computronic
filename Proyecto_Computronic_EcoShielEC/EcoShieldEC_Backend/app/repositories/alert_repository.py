from app.database.mongo_connection import alerts_collection

class AlertRepository:
    def get_latest(self):
        # Solo se encarga de la query técnica de MongoDB
        return alerts_collection.find_one(sort=[("_id", -1)])

    def create(self, alert_dict: dict):
        # Solo se encarga de la inserción técnica
        return alerts_collection.insert_one(alert_dict)
