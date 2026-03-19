from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, get_redis
from schemas import (
    ChatRequest, ChatResponse, ConversationResponse, 
    ConversationListResponse, MessageResponse
)
from models import User, Conversation, Message
from claude_service import claude_service
from typing import List
from datetime import datetime
import json

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    redis = Depends(get_redis)
):
    """
    Envoyer un message et recevoir une réponse de Claude
    """
    try:
        # Récupérer ou créer l'utilisateur
        user = db.query(User).filter(User.session_id == request.session_id).first()
        if not user:
            user = User(session_id=request.session_id)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Récupérer ou créer la conversation
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user.id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation non trouvée")
        else:
            conversation = Conversation(user_id=user.id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Sauvegarder le message de l'utilisateur
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        db.commit()
        
        # Récupérer l'historique de la conversation depuis Redis ou DB
        cache_key = f"conversation:{conversation.id}:history"
        cached_history = redis.get(cache_key)
        
        if cached_history:
            message_history = json.loads(cached_history)
        else:
            # Charger depuis la base de données
            messages = db.query(Message).filter(
                Message.conversation_id == conversation.id
            ).order_by(Message.timestamp).all()
            
            message_history = [
                {"role": msg.role, "content": msg.content}
                for msg in messages[:-1]  # Exclure le dernier message qu'on vient d'ajouter
            ]
        
        # Ajouter le nouveau message
        message_history.append({"role": "user", "content": request.message})
        
        # Générer la réponse avec Claude
        response_text, tokens_used = await claude_service.generate_response(message_history)
        
        # Sauvegarder la réponse
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            tokens_used=tokens_used
        )
        db.add(assistant_message)
        
        # Mettre à jour le timestamp de la conversation
        conversation.updated_at = datetime.utcnow()
        
        # Générer un titre si c'est la première interaction
        if not conversation.title and len(message_history) == 1:
            title = await claude_service.generate_conversation_title(request.message)
            conversation.title = title
        
        db.commit()
        db.refresh(assistant_message)
        
        # Mettre à jour le cache Redis
        message_history.append({"role": "assistant", "content": response_text})
        redis.setex(
            cache_key,
            settings.session_expire_minutes * 60,
            json.dumps(message_history)
        )
        
        return ChatResponse(
            message=response_text,
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            timestamp=assistant_message.timestamp
        )
        
    except Exception as e:
        db.rollback()
        print(f"Erreur dans /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{session_id}", response_model=List[ConversationListResponse])
async def get_conversations(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Récupérer toutes les conversations d'un utilisateur
    """
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        return []
    
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user.id,
        Conversation.is_active == True
    ).order_by(Conversation.updated_at.desc()).all()
    
    result = []
    for conv in conversations:
        message_count = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).count()
        
        result.append(ConversationListResponse(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=message_count
        ))
    
    return result

@router.get("/conversations/{session_id}/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    session_id: str,
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer une conversation spécifique avec tous ses messages
    """
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")
    
    return conversation

@router.delete("/conversations/{session_id}/{conversation_id}")
async def delete_conversation(
    session_id: str,
    conversation_id: int,
    db: Session = Depends(get_db),
    redis = Depends(get_redis)
):
    """
    Supprimer une conversation
    """
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")
    
    # Supprimer du cache Redis
    cache_key = f"conversation:{conversation_id}:history"
    redis.delete(cache_key)
    
    # Marquer comme inactive (soft delete)
    conversation.is_active = False
    db.commit()
    
    return {"message": "Conversation supprimée"}

@router.post("/conversations/new")
async def new_conversation(session_id: str, db: Session = Depends(get_db)):
    """
    Créer une nouvelle conversation
    """
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        user = User(session_id=session_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    conversation = Conversation(user_id=user.id, title="Nouvelle conversation")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return {"conversation_id": conversation.id}
