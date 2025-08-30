"""API dependencies."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import get_settings

settings = get_settings()
security = HTTPBasic()


def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    """Validate basic authentication credentials."""
    if (
        credentials.username == settings.basic_auth_username
        and credentials.password == settings.basic_auth_password
    ):
        return credentials.username
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Basic"},
    )