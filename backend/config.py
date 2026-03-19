from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str
    
    # Database
    database_url: str
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Application
    app_name: str = "Synapse Chat"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str
    
    # CORS
    allowed_origins: str = "http://localhost:5173"
    
    # Session
    session_expire_minutes: int = 60
    
    class Config:
        env_file = ".env"
        
    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

settings = Settings()
