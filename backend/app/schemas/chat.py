from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class MessageCreate(BaseModel):
    content: str = Field(..., max_length=4000)
    conversation_id: Optional[str] = None
    user_id: Optional[str] = "anonymous"


class MessageResponse(BaseModel):
    id: str
    content: str
    role: Literal["user", "assistant"]
    conversation_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    user_id: Optional[str] = "anonymous"


class ConversationResponse(BaseModel):
    id: str
    title: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    
    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    messages: List[MessageResponse] = []


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=4000)
    conversation_id: Optional[str] = None
    user_id: str = "anonymous"
    stream: bool = False
    use_rag: bool = False


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: Optional[List[dict]] = None


class DocumentUpload(BaseModel):
    filename: str
    content: str
    user_id: str = "anonymous"


class ProviderConfig(BaseModel):
    provider: Literal["claude", "openai", "ollama"]
    model: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    ai_provider: str
    rag_enabled: bool
    database_connected: bool
    redis_connected: bool
