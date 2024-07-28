from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class NotificationType(str, Enum):
    terminal = "terminal"
    email = "email"

class ScrapeSettings(BaseModel):
    page_limit: int
    proxy: Optional[str] = None

class NotificationConfig(BaseModel):
    notification_type: NotificationType
    recipients: List[str]

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class NotificationConfigDB(Base):
    __tablename__ = "notification_config"

    id = Column(Integer, primary_key=True, index=True)
    notification_type = Column(String, index=True)
    recipients = Column(Text)
