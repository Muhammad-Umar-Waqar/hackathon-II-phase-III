"""
Security utilities for the Todo application
"""
import re
from typing import Optional
from fastapi import HTTPException, status


class SecurityValidator:
    """Security validation utilities"""

    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128

    # Username requirements
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 30
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')

    # Email validation
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    # SQL injection patterns to detect
    SQL_INJECTION_PATTERNS = [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(\bINSERT\b.*\bINTO\b)",
        r"(\bDELETE\b.*\bFROM\b)",
        r"(--)",
        r"(;.*--)",
        r"(\bOR\b.*=.*)",
        r"('.*OR.*'.*=.*')"
    ]

    @classmethod
    def validate_password(cls, password: str) -> tuple[bool, Optional[str]]:
        """
        Validate password strength
        Returns: (is_valid, error_message)
        """
        if len(password) < cls.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {cls.MIN_PASSWORD_LENGTH} characters"

        if len(password) > cls.MAX_PASSWORD_LENGTH:
            return False, f"Password must be at most {cls.MAX_PASSWORD_LENGTH} characters"

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        # Check for at least one digit
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"

        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"

        return True, None

    @classmethod
    def validate_username(cls, username: str) -> tuple[bool, Optional[str]]:
        """
        Validate username format
        Returns: (is_valid, error_message)
        """
        if len(username) < cls.MIN_USERNAME_LENGTH:
            return False, f"Username must be at least {cls.MIN_USERNAME_LENGTH} characters"

        if len(username) > cls.MAX_USERNAME_LENGTH:
            return False, f"Username must be at most {cls.MAX_USERNAME_LENGTH} characters"

        if not cls.USERNAME_PATTERN.match(username):
            return False, "Username can only contain letters, numbers, hyphens, and underscores"

        return True, None

    @classmethod
    def validate_email(cls, email: str) -> tuple[bool, Optional[str]]:
        """
        Validate email format
        Returns: (is_valid, error_message)
        """
        if not cls.EMAIL_PATTERN.match(email):
            return False, "Invalid email format"

        if len(email) > 254:  # RFC 5321
            return False, "Email address is too long"

        return True, None

    @classmethod
    def check_sql_injection(cls, input_string: str) -> bool:
        """
        Check if input contains potential SQL injection patterns
        Returns: True if suspicious pattern detected
        """
        input_upper = input_string.upper()

        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, input_upper, re.IGNORECASE):
                return True

        return False

    @classmethod
    def sanitize_input(cls, input_string: str, max_length: int = 1000) -> str:
        """
        Sanitize user input by removing potentially dangerous characters
        """
        if cls.check_sql_injection(input_string):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input detected"
            )

        # Truncate to max length
        sanitized = input_string[:max_length]

        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')

        return sanitized.strip()

    @classmethod
    def validate_task_title(cls, title: str) -> tuple[bool, Optional[str]]:
        """
        Validate task title
        Returns: (is_valid, error_message)
        """
        if not title or len(title.strip()) == 0:
            return False, "Title cannot be empty"

        if len(title) > 200:
            return False, "Title must be 200 characters or less"

        if cls.check_sql_injection(title):
            return False, "Invalid characters in title"

        return True, None

    @classmethod
    def validate_task_description(cls, description: Optional[str]) -> tuple[bool, Optional[str]]:
        """
        Validate task description
        Returns: (is_valid, error_message)
        """
        if description is None:
            return True, None

        if len(description) > 1000:
            return False, "Description must be 1000 characters or less"

        if cls.check_sql_injection(description):
            return False, "Invalid characters in description"

        return True, None


def validate_content_type(content_type: str, allowed_types: list[str]) -> bool:
    """
    Validate content type against allowed types
    """
    return content_type in allowed_types


def generate_secure_headers() -> dict:
    """
    Generate secure HTTP headers
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
