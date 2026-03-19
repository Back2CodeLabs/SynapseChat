from abc import ABC, abstractmethod
from typing import List, Dict, AsyncGenerator


class AIProvider(ABC):
    """Interface abstraite pour tous les providers IA"""
    
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> str:
        """Génère une réponse à partir de l'historique de messages"""
        pass
    
    @abstractmethod
    async def generate_response_stream(
        self,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Génère une réponse en streaming"""
        pass
    
    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Génère un embedding pour un texte"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Vérifie si le provider est disponible"""
        pass
