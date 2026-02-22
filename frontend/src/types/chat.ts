// TypeScript types for chat functionality

export interface ToolCall {
  tool: string;
  parameters: Record<string, any>;
  requires_confirmation: boolean;
}

export interface Message {
  id: string;
  conversation_id: string;
  user_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  tool_calls?: ToolCall[];
  created_at: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  conversation_id?: string;
  content: string;
}

export interface ChatResponse {
  conversation_id: string;
  message_id: string;
  response: string;
  tool_calls: ToolCall[];
}

export interface ConversationListResponse {
  conversations: Conversation[];
}

export interface MessageListResponse {
  messages: Message[];
}
