import logging
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create logger
logger = logging.getLogger("todo_app")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
console_handler.setFormatter(console_formatter)

# File handler for all logs
file_handler = logging.FileHandler(
    log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
file_handler.setFormatter(file_formatter)

# File handler for errors only
error_handler = logging.FileHandler(
    log_dir / f"error_{datetime.now().strftime('%Y%m%d')}.log"
)
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
error_handler.setFormatter(error_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_handler)

def log_request(method: str, path: str, user_id: int = None):
    """Log incoming API requests"""
    user_info = f"user_id={user_id}" if user_id else "unauthenticated"
    logger.info(f"Request: {method} {path} ({user_info})")

def log_error(error: Exception, context: str = ""):
    """Log errors with context"""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def log_security_event(event: str, details: dict = None):
    """Log security-related events"""
    details_str = f" - {details}" if details else ""
    logger.warning(f"Security Event: {event}{details_str}")

def log_agent_invocation(conversation_id: str, user_id: str, message: str):
    """Log AI agent invocations"""
    logger.info(f"Agent Invocation: conversation_id={conversation_id}, user_id={user_id}, message_length={len(message)}")

def log_agent_response(conversation_id: str, user_id: str, response: str, tool_calls: list = None):
    """Log AI agent responses"""
    tool_count = len(tool_calls) if tool_calls else 0
    logger.info(f"Agent Response: conversation_id={conversation_id}, user_id={user_id}, response_length={len(response)}, tool_calls={tool_count}")

def log_tool_call(conversation_id: str, tool_name: str, parameters: dict):
    """Log tool call suggestions from agent"""
    logger.info(f"Tool Call Suggested: conversation_id={conversation_id}, tool={tool_name}, params={parameters}")

def log_agent_error(conversation_id: str, user_id: str, error: Exception):
    """Log agent-specific errors"""
    logger.error(f"Agent Error: conversation_id={conversation_id}, user_id={user_id}, error={str(error)}", exc_info=True)

