from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime
from ..models.conversation import Conversation, ConversationCreate, ConversationResponse
from ..utils.logger import logger


class ConversationService:
    """Service for managing conversations"""

    @staticmethod
    def create_conversation(db: Session, user_id: str) -> Conversation:
        """Create a new conversation for a user"""
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        logger.info(f"Created conversation: id={conversation.id}, user_id={user_id}")
        return conversation

    @staticmethod
    def get_conversation_by_id(db: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """Get a conversation by ID, ensuring it belongs to the user"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db.exec(statement).first()
        return conversation

    @staticmethod
    def get_user_conversations(db: Session, user_id: str, skip: int = 0, limit: int = 20) -> List[Conversation]:
        """Get all conversations for a user"""
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit)
        conversations = db.exec(statement).all()
        return list(conversations)

    @staticmethod
    def update_conversation_timestamp(db: Session, conversation_id: str) -> None:
        """Update the updated_at timestamp for a conversation"""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = db.exec(statement).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()
            db.add(conversation)
            db.commit()
