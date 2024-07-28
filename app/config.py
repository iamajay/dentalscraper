from app.models import NotificationType

class Config:
    STATIC_TOKEN = "08b03115-0e48-4336-a3ab-448b87a87d58"
    DEFAULT_NOTIFICATION_CONFIG = {
        "notification_type": NotificationType.terminal,
        "recipients": []
    }