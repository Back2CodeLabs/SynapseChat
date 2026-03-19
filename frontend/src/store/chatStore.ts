import { create } from 'zustand';
import type { Message, Conversation, AppConfig } from '../types';

interface ChatStore {
  // State
  conversations: Conversation[];
  currentConversation: Conversation | null;
  messages: Message[];
  isLoading: boolean;
  isSending: boolean;
  config: AppConfig;

  // Actions
  setConversations: (conversations: Conversation[]) => void;
  setCurrentConversation: (conversation: Conversation | null) => void;
  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;
  updateLastMessage: (content: string) => void;
  setIsLoading: (loading: boolean) => void;
  setIsSending: (sending: boolean) => void;
  updateConfig: (config: Partial<AppConfig>) => void;
  clearMessages: () => void;
}

const defaultConfig: AppConfig = {
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  userId: localStorage.getItem('userId') || `user_${Date.now()}`,
  aiProvider: (localStorage.getItem('aiProvider') as any) || 'claude',
  ollamaModel: localStorage.getItem('ollamaModel') || 'mistral',
  enableRAG: localStorage.getItem('enableRAG') === 'true',
  enableStreaming: localStorage.getItem('enableStreaming') !== 'false', // true par défaut
};

// Sauvegarder l'userId
localStorage.setItem('userId', defaultConfig.userId);

export const useChatStore = create<ChatStore>((set) => ({
  conversations: [],
  currentConversation: null,
  messages: [],
  isLoading: false,
  isSending: false,
  config: defaultConfig,

  setConversations: (conversations) => set({ conversations }),
  
  setCurrentConversation: (conversation) => 
    set({ 
      currentConversation: conversation,
      messages: conversation?.messages || []
    }),
  
  setMessages: (messages) => set({ messages }),
  
  addMessage: (message) => 
    set((state) => ({ 
      messages: [...state.messages, message] 
    })),
  
  updateLastMessage: (content) => 
    set((state) => {
      const messages = [...state.messages];
      if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        if (lastMessage.role === 'assistant') {
          lastMessage.content += content;
        }
      }
      return { messages };
    }),
  
  setIsLoading: (loading) => set({ isLoading: loading }),
  
  setIsSending: (sending) => set({ isSending: sending }),
  
  updateConfig: (newConfig) => 
    set((state) => {
      const config = { ...state.config, ...newConfig };
      
      // Sauvegarder dans localStorage
      if (newConfig.aiProvider) {
        localStorage.setItem('aiProvider', newConfig.aiProvider);
      }
      if (newConfig.ollamaModel) {
        localStorage.setItem('ollamaModel', newConfig.ollamaModel);
      }
      if (newConfig.enableRAG !== undefined) {
        localStorage.setItem('enableRAG', String(newConfig.enableRAG));
      }
      if (newConfig.enableStreaming !== undefined) {
        localStorage.setItem('enableStreaming', String(newConfig.enableStreaming));
      }
      
      return { config };
    }),
  
  clearMessages: () => set({ messages: [], currentConversation: null }),
}));