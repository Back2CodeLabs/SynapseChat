from typing import List, Dict, AsyncGenerator
from openai import AsyncOpenAI
from app.services.ai_provider import AIProvider
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """Provider pour l'API OpenAI"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.model = settings.OPENAI_MODEL
    
    def is_available(self) -> bool:
        return self.client is not None and bool(settings.OPENAI_API_KEY)
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> str:
        """Génère une réponse avec OpenAI"""
        if not self.is_available():
            raise ValueError("OpenAI API key not configured")
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4096,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise
    
    async def generate_response_stream(
        self,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Génère une réponse en streaming avec OpenAI"""
        if not self.is_available():
            raise ValueError("OpenAI API key not configured")
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4096,
                temperature=0.7,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            logger.error(f"Error streaming from OpenAI API: {e}")
            raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Génère un embedding avec OpenAI"""
        if not self.is_available():
            raise ValueError("OpenAI API key not configured")
        
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
