@echo off
REM Script de configuration pour Windows avec Ollama distant

echo ========================================
echo Configuration de Synapse Chat - Windows
echo ========================================
echo.

REM Créer le fichier .env backend
echo Creation du fichier backend\.env...
(
echo # Configuration pour Windows avec Ollama distant
echo.
echo # Application
echo APP_NAME=Synapse Chat
echo APP_VERSION=1.0.0
echo ENVIRONMENT=development
echo DEBUG=True
echo.
echo # Server
echo HOST=0.0.0.0
echo PORT=8000
echo.
echo # AI Provider - OLLAMA sur VM distante
echo AI_PROVIDER=ollama
echo.
echo # Ollama distant
echo OLLAMA_BASE_URL=http://localhost:11434
echo OLLAMA_MODEL=mistral
echo.
echo # Claude API (optionnel - décommenter si vous voulez l'utiliser)
echo # ANTHROPIC_API_KEY=votre_cle_api_anthropic
echo # CLAUDE_MODEL=claude-sonnet-4-20250514
echo.
echo # OpenAI API (optionnel)
echo # OPENAI_API_KEY=votre_cle_api_openai
echo # OPENAI_MODEL=gpt-4-turbo-preview
echo.
echo # RAG Configuration
echo ENABLE_RAG=True
echo EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
echo CHROMA_PERSIST_DIR=./data/chroma
echo MAX_CHUNKS_TO_RETRIEVE=5
echo.
echo # Database
echo DATABASE_URL=postgresql+asyncpg://synapsechat:synapsechat123@postgres:5432/synapsechat_db
echo DATABASE_POOL_SIZE=20
echo DATABASE_MAX_OVERFLOW=0
echo.
echo # Redis
echo REDIS_URL=redis://redis:6379/0
echo REDIS_SESSION_TTL=3600
echo.
echo # Security
echo SECRET_KEY=change-this-secret-key-in-production
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
echo.
echo # CORS
echo CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
echo.
echo # File Upload
echo MAX_UPLOAD_SIZE=10485760
echo ALLOWED_EXTENSIONS=[".pdf", ".txt", ".docx", ".md"]
echo.
echo # Conversation
echo MAX_CONVERSATION_HISTORY=20
echo MAX_MESSAGE_LENGTH=4000
) > backend\.env

echo [OK] Fichier backend\.env cree
echo.

REM Créer le fichier .env frontend
echo Creation du fichier frontend\.env...
echo VITE_API_URL=http://localhost:8000/api > frontend\.env
echo [OK] Fichier frontend\.env cree
echo.

echo ========================================
echo Configuration terminee !
echo ========================================
echo.
echo Votre configuration :
echo - Provider IA : Ollama (Mistral)
echo - Ollama URL  : http://localhost:11434
echo - RAG         : Active
echo.
echo Prochaine etape : Demarrer avec Docker
echo   docker-compose up -d
echo.
echo Ou utilisez le script : start-windows.bat
echo.
pause
