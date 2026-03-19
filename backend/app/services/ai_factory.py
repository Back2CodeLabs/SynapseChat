from app.services.ai_provider import AIProvider
from app.services.claude_provider import ClaudeProvider
from app.services.openai_provider import OpenAIProvider
from app.services.ollama_provider import OllamaProvider
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class AIProviderFactory:
    """Factory pour créer le bon provider IA selon la configuration"""
    
    _instance = None
    _provider: AIProvider = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIProviderFactory, cls).__new__(cls)
        return cls._instance
    
    def get_provider(self) -> AIProvider:
        """Retourne le provider configuré"""
        if self._provider is None:
            self._provider = self._create_provider()
        return self._provider
    
    def _create_provider(self) -> AIProvider:
        """Crée le provider selon la configuration"""
        provider_type = settings.AI_PROVIDER.lower()
        
        logger.info(f"Initializing AI provider: {provider_type}")
        
        if provider_type == "claude":
            provider = ClaudeProvider()
            if not provider.is_available():
                logger.warning("Claude provider not available, checking alternatives...")
                return self._get_fallback_provider()
            return provider
        
        elif provider_type == "openai":
            provider = OpenAIProvider()
            if not provider.is_available():
                logger.warning("OpenAI provider not available, checking alternatives...")
                return self._get_fallback_provider()
            return provider
        
        elif provider_type == "ollama":
            provider = OllamaProvider()
            if not provider.is_available():
                logger.warning("Ollama not available. Make sure Ollama is running.")
                return self._get_fallback_provider()
            return provider
        
        else:
            raise ValueError(f"Unknown AI provider: {provider_type}")
    
    def _get_fallback_provider(self) -> AIProvider:
        """Essaye les providers disponibles dans l'ordre de préférence"""
        # Essayer Claude
        claude = ClaudeProvider()
        if claude.is_available():
            logger.info("Falling back to Claude provider")
            return claude
        
        # Essayer OpenAI
        openai = OpenAIProvider()
        if openai.is_available():
            logger.info("Falling back to OpenAI provider")
            return openai
        
        # Essayer Ollama
        ollama = OllamaProvider()
        if ollama.is_available():
            logger.info("Falling back to Ollama provider")
            return ollama
        
        raise ValueError("No AI provider available. Please configure at least one provider.")
    
    def set_provider(self, provider_type: str):
        """Change le provider à la volée"""
        old_type = settings.AI_PROVIDER
        settings.AI_PROVIDER = provider_type
        
        try:
            self._provider = self._create_provider()
            logger.info(f"Provider changed from {old_type} to {provider_type}")
        except Exception as e:
            # Revenir à l'ancien provider en cas d'erreur
            settings.AI_PROVIDER = old_type
            logger.error(f"Failed to change provider: {e}")
            raise


# Instance globale
ai_factory = AIProviderFactory()
