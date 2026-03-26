from fastapi import FastAPI
from app.routers.mangrove_router import router as mangrove_router

app = FastAPI(
    title="EcoShieldEC API",
    version="1.0.0",
    description="Sistema de monitoreo inteligente de manglares"
)

# Registro de rutas
app.include_router(mangrove_router, prefix="/api/v1", tags=["Mangroves"])

@app.get("/", summary="Health Check")
def read_root():
    return {"message": "EcoShieldEC API is running 🚀"}
