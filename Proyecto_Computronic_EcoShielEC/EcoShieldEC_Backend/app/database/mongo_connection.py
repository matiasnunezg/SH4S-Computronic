import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    _client: MongoClient | None = None
    _db = None

    @classmethod
    def connect(cls):
        if cls._client is None:
            try:
                uri = os.getenv("MONGODB_ATLAS_URI")
                db_name = os.getenv("DATABASE_NAME", "ecosystem_db")

                if not uri:
                    raise ValueError("MONGODB_ATLAS_URI no está definida en el .env")

                cls._client = MongoClient(
                    uri,
                    serverSelectionTimeoutMS=5000
                )

                cls._client.server_info()

                cls._db = cls._client[db_name]

                print("✅ Conectado a MongoDB Atlas")

            except ServerSelectionTimeoutError:
                print("❌ Error: No se pudo conectar a MongoDB Atlas")
                raise

            except Exception as e:
                print(f"❌ Error inesperado en MongoDB: {e}")
                raise

    @classmethod
    def get_database(cls):
        if cls._db is None:
            cls.connect()

        if cls._db is None:
            raise RuntimeError("No se pudo inicializar la base de datos")

        return cls._db

    @classmethod
    def get_collection(cls, name: str):
        db = cls.get_database()
        if db is None:
            raise RuntimeError("Database no disponible")
        return db[name]


alerts_collection = MongoDB.get_collection("alerts")
