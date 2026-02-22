// ChatInterface - Main chat UI component

import React, { useState, useEffect } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { chatClient } from '../lib/chat-client';
import { Message, ToolCall } from '../types/chat';
import { taskAPI } from '../services/api';

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

  // Execute tool calls from AI response
  const executeToolCalls = async (toolCalls: ToolCall[]) => {
    const results: string[] = [];

    for (const toolCall of toolCalls) {
      try {
        const { tool, parameters } = toolCall;

        switch (tool) {
          case 'add_task':
            const newTask = await taskAPI.create({
              title: parameters.title,
              description: parameters.description || '',
              status: parameters.status || 'pending',
              due_date: parameters.due_date || null
            });
            results.push(`✅ Task created: "${parameters.title}"`);
            break;

          case 'list_tasks':
            const tasks = await taskAPI.getAll();
            const taskList = tasks.data.map((t: any) =>
              `- [${t.status}] ${t.title} (ID: ${t.id})`
            ).join('\n');
            results.push(`📋 Your tasks:\n${taskList || 'No tasks found'}`);
            break;

          case 'update_task':
            const updateData: any = {};
            if (parameters.title) updateData.title = parameters.title;
            if (parameters.description) updateData.description = parameters.description;
            if (parameters.status) updateData.status = parameters.status;
            if (parameters.due_date) updateData.due_date = parameters.due_date;

            await taskAPI.update(parameters.task_id, updateData);
            results.push(`✅ Task ${parameters.task_id} updated`);
            break;

          case 'complete_task':
            await taskAPI.update(parameters.task_id, { status: 'completed' });
            results.push(`✅ Task ${parameters.task_id} marked as completed`);
            break;

          case 'delete_task':
            await taskAPI.delete(parameters.task_id);
            results.push(`🗑️ Task ${parameters.task_id} deleted`);
            break;

          default:
            results.push(`⚠️ Unknown tool: ${tool}`);
        }
      } catch (err: any) {
        console.error(`Failed to execute ${toolCall.tool}:`, err);
        results.push(`❌ Failed to execute ${toolCall.tool}: ${err.response?.data?.detail || err.message}`);
      }
    }

    return results;
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

      // Execute tool calls if present
      if (response.tool_calls && response.tool_calls.length > 0) {
        const executionResults = await executeToolCalls(response.tool_calls);

        // Add execution results as a system message
        const systemMessage: Message = {
          id: `system-${Date.now()}`,
          conversation_id: response.conversation_id,
          user_id: '',
          role: 'system',
          content: executionResults.join('\n'),
          created_at: new Date().toISOString()
        };
        setMessages(prev => [...prev.slice(0, -1), systemMessage]);
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
