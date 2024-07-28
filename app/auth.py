from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import Config

security = HTTPBearer()
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != Config.STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return credentials.credentials