from typing import List, Dict, AsyncGenerator
from anthropic import AsyncAnthropic
from app.services.ai_provider import AIProvider
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ClaudeProvider(AIProvider):
    """Provider pour l'API Claude (Anthropic)"""
    
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None
        self.model = settings.CLAUDE_MODEL
    
    def is_available(self) -> bool:
        return self.client is not None and bool(settings.ANTHROPIC_API_KEY)
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> str:
        """Génère une réponse avec Claude"""
        if not self.is_available():
            raise ValueError("Claude API key not configured")
        
        try:
            # Convertir le format des messages
            formatted_messages = []
            system_message = None
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Appel à l'API Claude
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_message if system_message else "You are a helpful AI assistant.",
                messages=formatted_messages
            )
            
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            raise
    
    async def generate_response_stream(
        self,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Génère une réponse en streaming avec Claude"""
        if not self.is_available():
            raise ValueError("Claude API key not configured")
        
        try:
            # Convertir le format des messages
            formatted_messages = []
            system_message = None
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Streaming avec Claude
            async with self.client.messages.stream(
                model=self.model,
                max_tokens=4096,
                system=system_message if system_message else "You are a helpful AI assistant.",
                messages=formatted_messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        
        except Exception as e:
            logger.error(f"Error streaming from Claude API: {e}")
            raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Claude n'a pas d'API d'embedding native.
        On utilise sentence-transformers à la place.
        """
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(settings.EMBEDDING_MODEL)
        embedding = model.encode(text)
        return embedding.tolist()
