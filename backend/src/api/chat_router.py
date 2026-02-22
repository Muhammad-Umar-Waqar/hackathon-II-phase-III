from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import Optional, List
from slowapi import Limiter
from slowapi.util import get_remote_address
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from ..database import get_db
from ..models.conversation import ConversationResponse
from ..models.message import MessageCreate, MessageResponse
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..services.agent_service import AgentService
from ..utils.logger import logger, log_error, log_request

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
ALGORITHM = "HS256"

router = APIRouter()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

# Initialize agent service
agent_service = AgentService()


def verify_token(token: str) -> str:
    """
    Verify and decode a JWT token
    Returns user_id as string
    """
    try:
        logger.info(f"Verifying token: {token[:20]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        logger.info(f"Token decoded successfully, user_id: {user_id}")
        if user_id is None:
            logger.error("Token payload missing 'sub' field")
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user_id
    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.post("/chat")
@limiter.limit("30/minute")
async def send_chat_message(
    request: Request,
    message_data: MessageCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Send a message to the AI agent and receive a response.
    If no conversation_id is provided, a new conversation is created.
    """
    try:
        # Verify JWT and get user_id
        user_id = verify_token(credentials.credentials)
        log_request("POST", "/chat", user_id)

        # Validate message content
        if not message_data.content or not message_data.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content cannot be empty"
            )

        # Get or create conversation
        conversation = None
        if message_data.conversation_id:
            # Load existing conversation
            conversation = ConversationService.get_conversation_by_id(
                db, message_data.conversation_id, user_id
            )
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            # Create new conversation
            conversation = ConversationService.create_conversation(db, user_id)

        # Load conversation history
        conversation_history = MessageService.get_conversation_messages(
            db, conversation.id, user_id
        )

        # Format history for agent
        formatted_history = agent_service.format_conversation_history(conversation_history)

        # Save user message
        user_message = MessageService.create_message(
            db=db,
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=message_data.content
        )

        # Process message with agent
        agent_response = agent_service.process_message(
            user_message=message_data.content,
            conversation_history=formatted_history,
            conversation_id=conversation.id,
            user_id=user_id
        )

        # Save agent response
        assistant_message = MessageService.create_message(
            db=db,
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=agent_response["response"],
            tool_calls=agent_response.get("tool_calls")
        )

        # Update conversation timestamp
        ConversationService.update_conversation_timestamp(db, conversation.id)

        # Return response
        return {
            "conversation_id": conversation.id,
            "message_id": assistant_message.id,
            "response": agent_response["response"],
            "tool_calls": agent_response.get("tool_calls", [])
        }

    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "send_chat_message")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat message"
        )


@router.get("/conversations", response_model=List[ConversationResponse])
@limiter.limit("60/minute")
async def list_conversations(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    List all conversations for the authenticated user
    """
    try:
        user_id = verify_token(credentials.credentials)
        log_request("GET", "/conversations", user_id)

        conversations = ConversationService.get_user_conversations(
            db, user_id, skip=skip, limit=limit
        )
        return conversations

    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "list_conversations")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
@limiter.limit("60/minute")
async def get_conversation_messages(
    request: Request,
    conversation_id: str,
    limit: int = 100,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get all messages for a specific conversation
    """
    try:
        user_id = verify_token(credentials.credentials)
        log_request("GET", f"/conversations/{conversation_id}/messages", user_id)

        # Verify conversation ownership
        conversation = ConversationService.get_conversation_by_id(
            db, conversation_id, user_id
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Get messages
        messages = MessageService.get_conversation_messages(
            db, conversation_id, user_id, limit=limit
        )
        return messages

    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "get_conversation_messages")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages"
        )
