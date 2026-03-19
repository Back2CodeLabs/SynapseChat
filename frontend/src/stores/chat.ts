import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import { chatApi } from '@/services/api';
import type { Message, ConversationListItem } from '@/types';

export const useChatStore = defineStore('chat', () => {
  // State
  const sessionId = ref<string>('');
  const currentConversationId = ref<number | null>(null);
  const messages = ref<Message[]>([]);
  const conversations = ref<ConversationListItem[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Computed
  const hasMessages = computed(() => messages.value.length > 0);
  const currentConversation = computed(() => 
    conversations.value.find(c => c.id === currentConversationId.value)
  );

  // Actions
  function initSession() {
    let storedSessionId = localStorage.getItem('synapsechat_session_id');
    if (!storedSessionId) {
      storedSessionId = uuidv4();
      localStorage.setItem('synapsechat_session_id', storedSessionId);
    }
    sessionId.value = storedSessionId;
  }

  async function loadConversations() {
    try {
      conversations.value = await chatApi.getConversations(sessionId.value);
    } catch (err) {
      console.error('Erreur lors du chargement des conversations:', err);
      error.value = 'Impossible de charger les conversations';
    }
  }

  async function loadConversation(conversationId: number) {
    try {
      isLoading.value = true;
      const conversation = await chatApi.getConversation(sessionId.value, conversationId);
      messages.value = conversation.messages;
      currentConversationId.value = conversationId;
    } catch (err) {
      console.error('Erreur lors du chargement de la conversation:', err);
      error.value = 'Impossible de charger la conversation';
    } finally {
      isLoading.value = false;
    }
  }

  async function sendMessage(content: string) {
    if (!content.trim()) return;

    isLoading.value = true;
    error.value = null;

    // Ajouter le message de l'utilisateur immédiatement
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
      conversation_id: currentConversationId.value || 0,
    };
    messages.value.push(userMessage);

    try {
      const response = await chatApi.sendMessage({
        message: content,
        conversation_id: currentConversationId.value || undefined,
        session_id: sessionId.value,
      });

      // Mettre à jour l'ID de conversation si c'est une nouvelle conversation
      if (!currentConversationId.value) {
        currentConversationId.value = response.conversation_id;
        await loadConversations();
      }

      // Ajouter la réponse de l'assistant
      const assistantMessage: Message = {
        id: response.message_id,
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp,
        conversation_id: response.conversation_id,
      };
      messages.value.push(assistantMessage);

      // Mettre à jour le dernier message de la conversation dans la liste
      await loadConversations();
    } catch (err: any) {
      console.error('Erreur lors de l\'envoi du message:', err);
      error.value = err.response?.data?.detail || 'Impossible d\'envoyer le message';
      // Retirer le message de l'utilisateur en cas d'erreur
      messages.value.pop();
    } finally {
      isLoading.value = false;
    }
  }

  async function startNewConversation() {
    messages.value = [];
    currentConversationId.value = null;
  }

  async function deleteConversation(conversationId: number) {
    try {
      await chatApi.deleteConversation(sessionId.value, conversationId);
      if (currentConversationId.value === conversationId) {
        startNewConversation();
      }
      await loadConversations();
    } catch (err) {
      console.error('Erreur lors de la suppression:', err);
      error.value = 'Impossible de supprimer la conversation';
    }
  }

  return {
    // State
    sessionId,
    currentConversationId,
    messages,
    conversations,
    isLoading,
    error,
    // Computed
    hasMessages,
    currentConversation,
    // Actions
    initSession,
    loadConversations,
    loadConversation,
    sendMessage,
    startNewConversation,
    deleteConversation,
  };
});
