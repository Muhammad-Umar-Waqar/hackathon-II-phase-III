from typing import List, Dict, Any
from ..models.message import Message


class ContextBuilder:
    """Utility for rebuilding conversation context from database messages"""

    @staticmethod
    def build_context(messages: List[Message], max_messages: int = 100) -> List[Dict[str, str]]:
        """
        Build conversation context from message objects for agent processing

        Args:
            messages: List of Message objects from database
            max_messages: Maximum number of messages to include (default 100)

        Returns:
            List of dicts with 'role' and 'content' keys formatted for OpenAI
        """
        # Limit to max_messages (most recent)
        limited_messages = messages[-max_messages:] if len(messages) > max_messages else messages

        # Format for OpenAI API
        context = []
        for msg in limited_messages:
            context.append({
                "role": msg.role,
                "content": msg.content
            })

        return context

    @staticmethod
    def get_context_summary(messages: List[Message]) -> Dict[str, Any]:
        """
        Get summary statistics about conversation context

        Args:
            messages: List of Message objects

        Returns:
            Dict with context statistics
        """
        total_messages = len(messages)
        user_messages = sum(1 for msg in messages if msg.role == "user")
        assistant_messages = sum(1 for msg in messages if msg.role == "assistant")
        system_messages = sum(1 for msg in messages if msg.role == "system")

        total_chars = sum(len(msg.content) for msg in messages)

        return {
            "total_messages": total_messages,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "system_messages": system_messages,
            "total_characters": total_chars,
            "average_message_length": total_chars // total_messages if total_messages > 0 else 0
        }

    @staticmethod
    def truncate_context(messages: List[Message], max_tokens: int = 4000) -> List[Message]:
        """
        Truncate conversation context to fit within token limit
        Keeps most recent messages and removes oldest ones

        Args:
            messages: List of Message objects
            max_tokens: Approximate maximum tokens (using 4 chars per token estimate)

        Returns:
            Truncated list of messages
        """
        # Rough estimate: 1 token ≈ 4 characters
        max_chars = max_tokens * 4

        total_chars = 0
        truncated = []

        # Start from most recent and work backwards
        for msg in reversed(messages):
            msg_chars = len(msg.content)
            if total_chars + msg_chars <= max_chars:
                truncated.insert(0, msg)
                total_chars += msg_chars
            else:
                break

        return truncated
