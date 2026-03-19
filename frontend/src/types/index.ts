export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  conversation_id: string;
  created_at: string;
  response_time?: number; // Temps de réponse en secondes
}

export interface Conversation {
  id: string;
  title: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  messages?: Message[];
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  user_id: string;
  stream: boolean;
  use_rag: boolean;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  sources?: any[];
}

export interface Document {
  id: string;
  filename: string;
  chunk_count: number;
  created_at: string;
}

export interface AppConfig {
  apiUrl: string;
  userId: string;
  aiProvider: 'claude' | 'openai' | 'ollama';
  ollamaModel: string;
  enableRAG: boolean;
  enableStreaming: boolean;
}

export interface HealthStatus {
  status: string;
  version: string;
  ai_provider: string;
  ai_available: boolean;
  rag_enabled: boolean;
  database_connected: boolean;
}