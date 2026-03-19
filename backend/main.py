from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import init_db
from routes import router
import uvicorn

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API Backend pour Synapse Chat avec Claude AI"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialiser la base de données au démarrage"""
    init_db()
    print(f"✅ {settings.app_name} v{settings.app_version} démarrée")
    print(f"📚 Base de données initialisée")
    print(f"🌐 CORS configuré pour: {settings.origins_list}")

@app.get("/")
async def root():
    return {
        "message": f"Bienvenue sur {settings.app_name}",
        "version": settings.app_version,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
