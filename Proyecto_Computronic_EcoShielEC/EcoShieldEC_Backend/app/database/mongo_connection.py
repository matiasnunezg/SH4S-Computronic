from pymongo import MongoClient

# Conexión robusta con timeout
client = MongoClient(
    "mongodb://localhost:27017",
    serverSelectionTimeoutMS=5000
)

db = client["ecosystem_db"]
alerts_collection = db["alerts"]
