from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    role: str
    timestamp: datetime
    conversation_id: int
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True

class ConversationListResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: int
    
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[int] = None
    session_id: str

class ChatResponse(BaseModel):
    message: str
    conversation_id: int
    message_id: int
    timestamp: datetime
    
class UserSession(BaseModel):
    session_id: str
    user_id: int
    created_at: datetime
