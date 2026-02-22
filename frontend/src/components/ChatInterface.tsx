// ChatInterface - Main chat UI component

import React, { useState, useEffect } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { chatClient } from '../lib/chat-client';
import { Message } from '../types/chat';

interface ChatInterfaceProps {
  conversationId?: string;
  onConversationCreated?: (conversationId: string) => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  conversationId: initialConversationId,
  onConversationCreated
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>(initialConversationId);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load conversation history if conversationId is provided
  useEffect(() => {
    if (conversationId) {
      loadConversationHistory(conversationId);
    }
  }, [conversationId]);

  const loadConversationHistory = async (convId: string) => {
    try {
      setLoading(true);
      setError(null);
      const history = await chatClient.getConversationMessages(convId);
      setMessages(history);
    } catch (err: any) {
      console.error('Failed to load conversation history:', err);
      setError('Failed to load conversation history');
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    try {
      setLoading(true);
      setError(null);

      // Optimistically add user message to UI
      const tempUserMessage: Message = {
        id: `temp-${Date.now()}`,
        conversation_id: conversationId || '',
        user_id: '',
        role: 'user',
        content,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, tempUserMessage]);

      // Send message to backend
      const response = await chatClient.sendMessage({
        conversation_id: conversationId,
        content
      });

      // Update conversation ID if this was the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
        if (onConversationCreated) {
          onConversationCreated(response.conversation_id);
        }
      }

      // Reload conversation to get actual messages with IDs
      await loadConversationHistory(response.conversation_id);

    } catch (err: any) {
      console.error('Failed to send message:', err);
      setError(err.response?.data?.detail || 'Failed to send message');
      // Remove optimistic message on error
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="p-4 border-b bg-gray-50">
        <h2 className="text-xl font-semibold text-gray-800">
          Todo Assistant
        </h2>
        {conversationId && (
          <p className="text-xs text-gray-500 mt-1">
            Conversation ID: {conversationId.substring(0, 8)}...
          </p>
        )}
      </div>

      {/* Error display */}
      {error && (
        <div className="mx-4 mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Messages */}
      <MessageList messages={messages} loading={loading} />

      {/* Input */}
      <MessageInput
        onSend={handleSendMessage}
        disabled={loading}
        placeholder="Ask me about your tasks..."
      />
    </div>
  );
};
