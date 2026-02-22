from sqlmodel import Session, select
from typing import Optional, List, Dict, Any
from ..models.message import Message, MessageCreate, MessageResponse
from ..utils.logger import logger


class MessageService:
    """Service for managing messages"""

    @staticmethod
    def create_message(
        db: Session,
        conversation_id: str,
        user_id: str,
        role: str,
        content: str,
        tool_calls: Optional[List[Dict[str, Any]]] = None
    ) -> Message:
        """Create a new message in a conversation"""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        logger.info(f"Created message: id={message.id}, conversation_id={conversation_id}, role={role}")
        return message

    @staticmethod
    def get_conversation_messages(
        db: Session,
        conversation_id: str,
        user_id: str,
        limit: int = 100
    ) -> List[Message]:
        """Get all messages for a conversation, ensuring user owns the conversation"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.created_at.asc()).limit(limit)
        messages = db.exec(statement).all()
        return list(messages)

    @staticmethod
    def get_message_by_id(db: Session, message_id: str, user_id: str) -> Optional[Message]:
        """Get a message by ID, ensuring it belongs to the user"""
        statement = select(Message).where(
            Message.id == message_id,
            Message.user_id == user_id
        )
        message = db.exec(statement).first()
        return message
