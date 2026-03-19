from typing import List, Dict, AsyncGenerator
import httpx
from app.services.ai_provider import AIProvider
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OllamaProvider(AIProvider):
    """Provider pour Ollama (LLM local)"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
    
    def is_available(self) -> bool:
        """Vérifie si Ollama est accessible"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> str:
        """Génère une réponse avec Ollama"""
        if not self.is_available():
            raise ValueError("Ollama is not available. Make sure it's running.")
        
        try:
            # Convertir les messages en prompt
            prompt = self._messages_to_prompt(messages)
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                if response.status_code != 200:
                    raise ValueError(f"Ollama API error: {response.status_code}")
                
                result = response.json()
                return result.get("response", "")
        
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise
    
    async def generate_response_stream(
        self,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Génère une réponse en streaming avec Ollama"""
        if not self.is_available():
            raise ValueError("Ollama is not available. Make sure it's running.")
        
        try:
            prompt = self._messages_to_prompt(messages)
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": True
                    }
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
        
        except Exception as e:
            logger.error(f"Error streaming from Ollama API: {e}")
            raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Génère un embedding avec Ollama"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/embeddings",
                    json={
                        "model": self.model,
                        "prompt": text
                    }
                )
                
                if response.status_code != 200:
                    # Fallback sur sentence-transformers
                    from sentence_transformers import SentenceTransformer
                    model = SentenceTransformer(settings.EMBEDDING_MODEL)
                    embedding = model.encode(text)
                    return embedding.tolist()
                
                result = response.json()
                return result.get("embedding", [])
        
        except Exception as e:
            logger.warning(f"Ollama embedding failed, using sentence-transformers: {e}")
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer(settings.EMBEDDING_MODEL)
            embedding = model.encode(text)
            return embedding.tolist()
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convertit la liste de messages en un prompt unique pour Ollama"""
        prompt_parts = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
