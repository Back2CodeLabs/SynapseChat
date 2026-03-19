from typing import List, Dict, Optional, AsyncGenerator
from app.services.ai_factory import ai_factory
from app.services.rag_service import rag_service
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service principal pour gérer les conversations"""
    
    def __init__(self):
        self.ai_provider = ai_factory.get_provider()
        self.rag_service = rag_service
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        use_rag: bool = False,
        user_id: Optional[str] = None,
        stream: bool = False
    ) -> str:
        """Génère une réponse du chatbot"""
        
        # Enrichir avec RAG si demandé
        if use_rag and self.rag_service and messages:
            enhanced_messages = await self._enhance_with_rag(messages, user_id)
        else:
            enhanced_messages = messages
        
        # Générer la réponse
        try:
            response = await self.ai_provider.generate_response(
                messages=enhanced_messages,
                stream=stream
            )
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def generate_response_stream(
        self,
        messages: List[Dict[str, str]],
        use_rag: bool = False,
        user_id: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Génère une réponse en streaming"""
        
        # Enrichir avec RAG si demandé
        if use_rag and self.rag_service and messages:
            enhanced_messages = await self._enhance_with_rag(messages, user_id)
        else:
            enhanced_messages = messages
        
        # Streamer la réponse
        try:
            async for chunk in self.ai_provider.generate_response_stream(enhanced_messages):
                yield chunk
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise
    
    async def _enhance_with_rag(
        self,
        messages: List[Dict[str, str]],
        user_id: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Enrichit les messages avec le contexte RAG"""
        if not messages:
            return messages
        
        # Récupérer le dernier message utilisateur
        last_user_message = None
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break
        
        if not last_user_message:
            return messages
        
        # Rechercher le contexte pertinent
        context = self.rag_service.get_context_for_query(last_user_message, user_id)
        
        if not context:
            return messages
        
        # Ajouter le contexte au message système
        enhanced_messages = messages.copy()
        
        # Vérifier s'il y a déjà un message système
        has_system = any(msg["role"] == "system" for msg in enhanced_messages)
        
        rag_prompt = f"""You have access to the following context from the knowledge base:

{context}

Use this information to answer the user's question when relevant. If the context doesn't contain relevant information, rely on your general knowledge."""
        
        if has_system:
            # Ajouter au message système existant
            for msg in enhanced_messages:
                if msg["role"] == "system":
                    msg["content"] += f"\n\n{rag_prompt}"
                    break
        else:
            # Créer un nouveau message système
            enhanced_messages.insert(0, {
                "role": "system",
                "content": rag_prompt
            })
        
        return enhanced_messages
    
    def prepare_messages(
        self,
        conversation_history: List[Dict[str, str]],
        new_message: str,
        system_prompt: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Prépare les messages pour l'IA"""
        messages = []
        
        # Message système
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": "You are a helpful, knowledgeable, and friendly AI assistant."
            })
        
        # Historique de conversation (limité)
        max_history = settings.MAX_CONVERSATION_HISTORY
        recent_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history
        
        messages.extend(recent_history)
        
        # Nouveau message
        messages.append({"role": "user", "content": new_message})
        
        return messages


# Instance globale
chat_service = ChatService()
