"""
FastAPI dependencies — auth + admin checks
"""
import os
from fastapi import Request, Header, HTTPException
from fastapi.responses import RedirectResponse
from backend.models.schemas import UserSession


def get_current_user(request: Request) -> UserSession:
    """
    Reads session cookie and returns the current user.
    Redirects to /login if session is missing or invalid.
    """
    user = request.session.get("user")
    if not user:
        # Return redirect response — caller must raise this
        raise HTTPException(status_code=302, headers={"Location": "/login"})
    return UserSession(**user)


def require_admin(request: Request) -> UserSession:
    """Requires the current user to have admin role."""
    user = get_current_user(request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def verify_admin_key(x_admin_key: str = Header(default=None)) -> bool:
    """
    Fallback key-based auth for programmatic/curl access.
    Accepts either a valid session OR the X-Admin-Key header.
    """
    expected = os.getenv("ADMIN_PASSWORD", "changeme")
    if x_admin_key != expected:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    return True
