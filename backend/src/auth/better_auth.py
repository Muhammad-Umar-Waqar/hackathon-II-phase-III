"""
Better Auth session verification for FastAPI backend
"""
from fastapi import HTTPException, status, Request
from sqlalchemy import text
from datetime import datetime
import os
from dotenv import load_dotenv
from urllib.parse import unquote

load_dotenv()

def verify_better_auth_session(request: Request) -> str:
    """
    Verify Better Auth session from cookie
    Returns user_id (TEXT) if valid
    """
    # Get session token from cookie
    session_cookie = request.cookies.get("better-auth.session_token")

    print(f"[DEBUG] Raw cookie value: {session_cookie}")

    if not session_cookie:
        print("[DEBUG] No session cookie found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # URL decode the cookie value
    session_token = unquote(session_cookie)
    print(f"[DEBUG] Decoded session token: {session_token}")

    # Better Auth cookie format: sessionId.signature
    # We need just the sessionId part (before the first dot)
    if '.' in session_token:
        session_id = session_token.split('.')[0]
    else:
        session_id = session_token

    print(f"[DEBUG] Extracted session ID: {session_id}")

    # Query the database to verify the session
    from ..database import engine

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT "userId", "expiresAt"
                    FROM session
                    WHERE id = :session_id
                """),
                {"session_id": session_id}
            )

            row = result.fetchone()

            if not row:
                print(f"[DEBUG] No session found in database for ID: {session_id}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid session"
                )

            user_id, expires_at = row
            print(f"[DEBUG] Found session - User ID: {user_id}, Expires: {expires_at}")

            # Check if session is expired
            if expires_at < datetime.utcnow():
                print(f"[DEBUG] Session expired")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Session expired"
                )

            print(f"[DEBUG] Session valid, returning user_id: {user_id}")
            return user_id

    except HTTPException:
        raise
    except Exception as e:
        print(f"[DEBUG] Session verification error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session verification failed"
        )



