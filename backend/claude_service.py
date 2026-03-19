from anthropic import Anthropic
from config import settings
from typing import List, Dict
import json

class ClaudeService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-sonnet-4-20250514"
        self.max_tokens = 4096
        
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: str = None
    ) -> tuple[str, int]:
        """
        Générer une réponse avec Claude
        
        Args:
            messages: Liste des messages de la conversation
            system_prompt: Prompt système optionnel
            
        Returns:
            tuple: (réponse, nombre de tokens utilisés)
        """
        try:
            # Préparer le prompt système par défaut
            if system_prompt is None:
                system_prompt = """Tu es un assistant IA avancé et utile. 
Tu réponds de manière claire, précise et professionnelle.
Tu te souviens du contexte de la conversation et tu peux faire référence aux messages précédents.
Tu es capable d'aider sur une grande variété de sujets."""

            # Appeler l'API Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=messages
            )
            
            # Extraire la réponse
            assistant_message = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            return assistant_message, tokens_used
            
        except Exception as e:
            print(f"Erreur lors de l'appel à Claude: {e}")
            raise
    
    async def generate_conversation_title(self, first_message: str) -> str:
        """
        Générer un titre pour la conversation basé sur le premier message
        
        Args:
            first_message: Premier message de l'utilisateur
            
        Returns:
            str: Titre généré
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=50,
                messages=[{
                    "role": "user",
                    "content": f"Génère un titre court (4-6 mots maximum) pour une conversation qui commence par: '{first_message}'. Réponds uniquement avec le titre, sans guillemets."
                }]
            )
            
            title = response.content[0].text.strip()
            return title[:100]  # Limiter à 100 caractères
            
        except Exception as e:
            print(f"Erreur lors de la génération du titre: {e}")
            return "Nouvelle conversation"

claude_service = ClaudeService()
