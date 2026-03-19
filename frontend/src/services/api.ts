import axios from 'axios';
import type { 
  ChatRequest, 
  ChatResponse, 
  Conversation, 
  Document,
  HealthStatus 
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatApi = {
  // Chat endpoints
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const { data } = await api.post<ChatResponse>('/chat', request);
    return data;
  },

  async sendMessageStream(
    request: ChatRequest,
    onChunk: (chunk: string) => void,
    onComplete: (conversationId: string) => void
  ): Promise<void> {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) return;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6));
          if (data.chunk) {
            onChunk(data.chunk);
          }
          if (data.done) {
            onComplete(data.conversation_id);
          }
        }
      }
    }
  },

  // Conversation endpoints
  async getConversations(userId: string, limit = 50): Promise<Conversation[]> {
    const { data } = await api.get<Conversation[]>('/conversations', {
      params: { user_id: userId, limit },
    });
    return data;
  },

  async getConversation(conversationId: string): Promise<Conversation> {
    const { data } = await api.get<Conversation>(`/conversations/${conversationId}`);
    return data;
  },

  async deleteConversation(conversationId: string): Promise<void> {
    await api.delete(`/conversations/${conversationId}`);
  },

  // Document endpoints
  async uploadDocument(file: File, userId: string): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    const { data } = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return data;
  },

  async getDocuments(userId: string): Promise<Document[]> {
    const { data } = await api.get<Document[]>('/documents', {
      params: { user_id: userId },
    });
    return data;
  },

  // Health check
  async getHealth(): Promise<HealthStatus> {
    const { data } = await api.get<HealthStatus>('/health');
    return data;
  },

  // Provider management
  async changeProvider(provider: string): Promise<any> {
    const { data } = await api.post('/provider/change', null, {
      params: { provider },
    });
    return data;
  },

  // Ollama model management
  async getOllamaModels(): Promise<string[]> {
    try {
      const { data } = await api.get('/ollama/models');
      return data.models || [];
    } catch (error) {
      console.error('Error fetching Ollama models:', error);
      return [];
    }
  },

  async changeOllamaModel(model: string): Promise<any> {
    const { data } = await api.post('/ollama/model/change', null, {
      params: { model },
    });
    return data;
  },
};