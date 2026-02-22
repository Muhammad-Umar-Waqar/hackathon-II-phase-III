// API client for chat endpoints

import axios from 'axios';
import { ChatRequest, ChatResponse, Conversation, Message } from '../types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1';

// Get auth token from localStorage or session
const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
};

// Create axios instance with auth header
const createAuthHeaders = () => {
  const token = getAuthToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const chatClient = {
  /**
   * Send a message to the chat endpoint
   */
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await axios.post(
      `${API_BASE_URL}/chat`,
      request,
      { headers: createAuthHeaders() }
    );
    return response.data;
  },

  /**
   * Get list of user's conversations
   */
  getConversations: async (skip: number = 0, limit: number = 20): Promise<Conversation[]> => {
    const response = await axios.get(
      `${API_BASE_URL}/conversations`,
      {
        params: { skip, limit },
        headers: createAuthHeaders()
      }
    );
    return response.data;
  },

  /**
   * Get messages for a specific conversation
   */
  getConversationMessages: async (conversationId: string, limit: number = 100): Promise<Message[]> => {
    const response = await axios.get(
      `${API_BASE_URL}/conversations/${conversationId}/messages`,
      {
        params: { limit },
        headers: createAuthHeaders()
      }
    );
    return response.data;
  }
};
