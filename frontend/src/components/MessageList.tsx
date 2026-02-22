// MessageList component for displaying conversation history

import React, { useEffect, useRef } from 'react';
import { Message, ToolCall } from '../types/chat';

interface MessageListProps {
  messages: Message[];
  loading?: boolean;
}

const ToolCallDisplay: React.FC<{ toolCalls: ToolCall[] }> = ({ toolCalls }) => {
  if (!toolCalls || toolCalls.length === 0) return null;

  return (
    <div className="mt-2 space-y-2">
      {toolCalls.map((toolCall, index) => (
        <div key={index} className="bg-blue-50 border border-blue-200 rounded p-2 text-sm">
          <div className="font-semibold text-blue-700">
            Tool: {toolCall.tool}
          </div>
          <div className="text-gray-600">
            Parameters: {JSON.stringify(toolCall.parameters)}
          </div>
          {toolCall.requires_confirmation && (
            <div className="text-orange-600 text-xs mt-1">
              ⚠️ Requires confirmation
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export const MessageList: React.FC<MessageListProps> = ({ messages, loading = false }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 && !loading && (
        <div className="text-center text-gray-500 mt-8">
          No messages yet. Start a conversation!
        </div>
      )}

      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[70%] rounded-lg p-3 ${
              message.role === 'user'
                ? 'bg-blue-500 text-white'
                : message.role === 'assistant'
                ? 'bg-gray-200 text-gray-800'
                : 'bg-yellow-100 text-gray-800'
            }`}
          >
            <div className="text-xs opacity-70 mb-1">
              {message.role === 'user' ? 'You' : message.role === 'assistant' ? 'Assistant' : 'System'}
            </div>
            <div className="whitespace-pre-wrap">{message.content}</div>
            {message.tool_calls && <ToolCallDisplay toolCalls={message.tool_calls} />}
            <div className="text-xs opacity-70 mt-1">
              {new Date(message.created_at).toLocaleTimeString()}
            </div>
          </div>
        </div>
      ))}

      {loading && (
        <div className="flex justify-start">
          <div className="bg-gray-200 rounded-lg p-3">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};
