from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["ecosystem_db"] # Nombre de la base de datos
alerts_collection = db["alerts"] # Nombre de la colección (la "tabla")

