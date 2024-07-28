from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models import NotificationConfig, NotificationType, NotificationConfigDB
from app.config import Config
from app.database import SessionLocal, init_db

router = APIRouter()

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != Config.STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return credentials.credentials

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/notification/config")
async def set_notification_config(config: NotificationConfig, token: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_config = db.query(NotificationConfigDB).first()
    if db_config:
        db_config.notification_type = config.notification_type.value
        db_config.recipients = ",".join(config.recipients)
    else:
        db_config = NotificationConfigDB(
            notification_type=config.notification_type.value,
            recipients=",".join(config.recipients)
        )
        db.add(db_config)
    db.commit()
    return {"message": "Notification configuration updated successfully"}

@router.get("/notification/config")
async def get_notification_config(token: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_config = db.query(NotificationConfigDB).first()
    if db_config:
        return {
            "notification_type": db_config.notification_type,
            "recipients": db_config.recipients.split(",")
        }
    return Config.DEFAULT_NOTIFICATION_CONFIG
