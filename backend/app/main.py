from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import init_db, check_db_connection
from app.api import chat
from app.services.ai_factory import ai_factory

# Configuration du logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Startup
    logger.info("Starting application...")
    
    # Initialiser la base de données
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    # Vérifier le provider IA
    try:
        provider = ai_factory.get_provider()
        logger.info(f"AI Provider initialized: {settings.AI_PROVIDER}")
    except Exception as e:
        logger.error(f"Failed to initialize AI provider: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/api/health")
async def health():
    """Endpoint de santé détaillé"""
    db_connected = await check_db_connection()
    
    try:
        provider = ai_factory.get_provider()
        ai_available = provider.is_available()
    except:
        ai_available = False
    
    return {
        "status": "healthy" if (db_connected and ai_available) else "degraded",
        "version": settings.APP_VERSION,
        "ai_provider": settings.AI_PROVIDER,
        "ai_available": ai_available,
        "rag_enabled": settings.ENABLE_RAG,
        "database_connected": db_connected,
    }


@app.post("/api/provider/change")
async def change_provider(provider: str):
    """Change le provider IA à la volée"""
    try:
        ai_factory.set_provider(provider)
        return {"status": "success", "provider": provider}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/ollama/models")
async def get_ollama_models():
    """Liste les modèles Ollama disponibles"""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                return {
                    "status": "success",
                    "models": models,
                    "current": settings.OLLAMA_MODEL
                }
            else:
                return {"status": "error", "message": "Failed to fetch models"}
    except Exception as e:
        logger.error(f"Error fetching Ollama models: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/api/ollama/model/change")
async def change_ollama_model(model: str):
    """Change le modèle Ollama actif"""
    try:
        settings.OLLAMA_MODEL = model
        # Réinitialiser le provider pour prendre en compte le nouveau modèle
        if settings.AI_PROVIDER == "ollama":
            ai_factory._provider = None
            ai_factory.get_provider()
        return {"status": "success", "model": model}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
