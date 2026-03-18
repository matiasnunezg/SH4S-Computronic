from fastapi import FastAPI
from app.routers import mangrove_router

app = FastAPI()

app.include_router(mangrove_router.router)

@app.get("/")
def read_root():
    return {"message": "EcoShieldEC API is running"}
