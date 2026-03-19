from pydantic_settings import BaseSettings
from typing import List, Literal


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Synapse Chat"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # AI Provider
    AI_PROVIDER: Literal["claude", "openai", "ollama"] = "claude"

    # Claude API
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    
    # OpenAI API
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: Literal["mistral", "deepseek-coder:6.7b", "qwen2.5-coder:7b", "codestral"] = "mistral"
    
    # RAG Configuration
    ENABLE_RAG: bool = True
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    MAX_CHUNKS_TO_RETRIEVE: int = 5
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://synapsechat:synapsechat123@localhost:5432/synapsechat_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_SESSION_TTL: int = 3600
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".docx", ".md"]
    
    # Conversation
    MAX_CONVERSATION_HISTORY: int = 20
    MAX_MESSAGE_LENGTH: int = 4000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
