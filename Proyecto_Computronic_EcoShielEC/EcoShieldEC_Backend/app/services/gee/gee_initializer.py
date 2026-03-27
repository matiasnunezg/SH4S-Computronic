import ee
import os
from dotenv import load_dotenv

load_dotenv()

class GEEInitializer:
    _initialized = False

    @classmethod
    def initialize(cls):
        if cls._initialized:
            return

        try:
            project_id = os.getenv("GEE_PROJECT_ID")
            key_path = os.getenv("GEE_JSON_KEY_PATH")

            if not project_id or not key_path:
                raise ValueError("Faltan variables GEE en el .env")

            if not os.path.exists(key_path):
                raise FileNotFoundError(f"No se encontró el JSON en {key_path}")

            credentials = ee.ServiceAccountCredentials(
                email=None,  # GEE lo toma del JSON
                key_file=key_path
            )

            ee.Initialize(credentials, project=project_id)

            cls._initialized = True

            print("🌍 GEE inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando GEE: {e}")
            raise
