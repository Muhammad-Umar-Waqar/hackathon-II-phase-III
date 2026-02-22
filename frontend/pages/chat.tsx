// Chat page

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { ChatInterface } from '../src/components/ChatInterface';
import { chatClient } from '../src/lib/chat-client';
import { Conversation } from '../src/types/chat';

export default function ChatPage() {
  const router = useRouter();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversationId, setSelectedConversationId] = useState<string | undefined>();
  const [showConversationList, setShowConversationList] = useState(false);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState<{ name?: string; email?: string } | null>(null);

  // Check authentication and load user info
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      const username = localStorage.getItem('username');

      if (!token) {
        router.push('/login');
      } else {
        setUser({ name: username || '', email: username || '' });
      }
    }
  }, []);

  // Load user's conversations on mount
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      setLoading(true);
      const convs = await chatClient.getConversations();
      setConversations(convs);
    } catch (err) {
      console.error('Failed to load conversations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleConversationCreated = (conversationId: string) => {
    setSelectedConversationId(conversationId);
    loadConversations(); // Refresh conversation list
  };

  const handleSelectConversation = (conversationId: string) => {
    setSelectedConversationId(conversationId);
    setShowConversationList(false);
  };

  const handleNewConversation = () => {
    setSelectedConversationId(undefined);
    setShowConversationList(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-4">
              <h1 className="text-xl font-semibold text-gray-900">AI Chat Assistant</h1>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-700 hidden md:inline">
                {user?.name || user?.email}
              </span>
              <button
                onClick={() => router.push('/')}
                className="text-sm bg-gray-500 hover:bg-gray-600 text-white py-1 px-3 rounded-md transition-colors"
              >
                📋 Tasks
              </button>
              <button
                onClick={handleLogout}
                className="text-sm bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded-md transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto p-4">
        <div className="flex gap-4 h-[calc(100vh-8rem)]">
          {/* Sidebar - Conversation List */}
          <div className={`${showConversationList ? 'block' : 'hidden'} md:block w-full md:w-64 bg-white rounded-lg shadow-lg p-4 overflow-y-auto`}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-semibold text-gray-800">Conversations</h3>
              <button
                onClick={handleNewConversation}
                className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
              >
                New
              </button>
            </div>

            {loading && <div className="text-gray-500 text-sm">Loading...</div>}

            <div className="space-y-2">
              {conversations.map((conv) => (
                <button
                  key={conv.id}
                  onClick={() => handleSelectConversation(conv.id)}
                  className={`w-full text-left p-3 rounded border ${
                    selectedConversationId === conv.id
                      ? 'bg-blue-50 border-blue-300'
                      : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                  }`}
                >
                  <div className="text-sm font-medium text-gray-800 truncate">
                    {conv.id.substring(0, 8)}...
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {new Date(conv.updated_at).toLocaleDateString()}
                  </div>
                </button>
              ))}

              {conversations.length === 0 && !loading && (
                <div className="text-gray-500 text-sm text-center py-4">
                  No conversations yet
                </div>
              )}
            </div>
          </div>

          {/* Main Chat Area */}
          <div className="flex-1 flex flex-col">
            {/* Mobile toggle button */}
            <button
              onClick={() => setShowConversationList(!showConversationList)}
              className="md:hidden mb-4 px-4 py-2 bg-white rounded-lg shadow"
            >
              {showConversationList ? 'Hide' : 'Show'} Conversations
            </button>

            <ChatInterface
              conversationId={selectedConversationId}
              onConversationCreated={handleConversationCreated}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
