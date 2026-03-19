import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader2, Settings, FileUp } from 'lucide-react';
import { useChatStore } from '../store/chatStore';
import { chatApi } from '../services/api';
import MessageList from './MessageList';
import SettingsPanel from './SettingsPanel';
import type { Message } from '../types';

const ChatInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const {
    messages,
    currentConversation,
    isSending,
    config,
    addMessage,
    updateLastMessage,
    setIsSending,
    setCurrentConversation,
  } = useChatStore();

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async () => {
    if (!input.trim() || isSending) return;

    const userMessage: Message = {
      id: `temp_${Date.now()}`,
      content: input.trim(),
      role: 'user',
      conversation_id: currentConversation?.id || '',
      created_at: new Date().toISOString(),
    };

    addMessage(userMessage);
    setInput('');
    setIsSending(true);

    try {
      const request = {
        message: input.trim(),
        conversation_id: currentConversation?.id,
        user_id: config.userId,
        stream: config.enableStreaming,
        use_rag: config.enableRAG,
      };

      if (config.enableStreaming) {
        // Ajouter un message assistant vide pour le streaming
        const assistantMessage: Message = {
          id: `temp_assistant_${Date.now()}`,
          content: '',
          role: 'assistant',
          conversation_id: currentConversation?.id || '',
          created_at: new Date().toISOString(),
        };
        addMessage(assistantMessage);

        await chatApi.sendMessageStream(
          request,
          (chunk) => {
            updateLastMessage(chunk);
          },
          (conversationId) => {
            if (!currentConversation) {
              setCurrentConversation({ 
                id: conversationId,
                title: input.slice(0, 50),
                user_id: config.userId,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString(),
                message_count: 2
              });
            }
          }
        );
      } else {
        const response = await chatApi.sendMessage(request);

        const assistantMessage: Message = {
          id: `assistant_${Date.now()}`,
          content: response.message,
          role: 'assistant',
          conversation_id: response.conversation_id,
          created_at: new Date().toISOString(),
        };
        addMessage(assistantMessage);

        if (!currentConversation) {
          setCurrentConversation({
            id: response.conversation_id,
            title: input.slice(0, 50),
            user_id: config.userId,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            message_count: 2
          });
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage({
        id: `error_${Date.now()}`,
        content: 'Erreur lors de l\'envoi du message. Veuillez réessayer.',
        role: 'assistant',
        conversation_id: currentConversation?.id || '',
        created_at: new Date().toISOString(),
      });
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Synapse Chat</h1>
          <p className="text-sm text-gray-500">
            Provider: {config.aiProvider} | RAG: {config.enableRAG ? 'Activé' : 'Désactivé'}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowUpload(!showUpload)}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            title="Upload documents"
          >
            <FileUp size={20} className="text-gray-600" />
          </button>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            title="Paramètres"
          >
            <Settings size={20} className="text-gray-600" />
          </button>
        </div>
      </header>

      {/* Settings Panel */}
      {showSettings && (
        <SettingsPanel onClose={() => setShowSettings(false)} />
      )}

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3 items-end">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Posez votre question..."
              className="flex-1 resize-none rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={1}
              style={{
                minHeight: '48px',
                maxHeight: '200px',
              }}
              disabled={isSending}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isSending}
              className="bg-blue-600 text-white rounded-lg px-4 py-3 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              {isSending ? (
                <Loader2 size={20} className="animate-spin" />
              ) : (
                <Send size={20} />
              )}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Appuyez sur Entrée pour envoyer, Maj+Entrée pour une nouvelle ligne
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
