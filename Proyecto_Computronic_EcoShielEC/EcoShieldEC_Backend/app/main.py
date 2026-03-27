from fastapi import FastAPI
from app.routers.mangrove_router import router as mangrove_router

# 🔥 NUEVO
from app.services.gee.gee_initializer import GEEInitializer

app = FastAPI(
    title="EcoShieldEC API",
    version="1.0.0",
    description="Sistema de monitoreo inteligente de manglares"
)

# 🔥 Inicialización al arrancar la app
@app.on_event("startup")
def startup_event():
    try:
        GEEInitializer.initialize()
        print("🚀 Sistema listo")
    except Exception as e:
        print(f"❌ Error en startup: {e}")
        raise

# Registro de rutas
app.include_router(mangrove_router, prefix="/api/v1", tags=["Mangroves"])

@app.get("/", summary="Health Check")
def read_root():
    return {"message": "EcoShieldEC API is running"}
