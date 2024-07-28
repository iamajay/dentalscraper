from abc import ABC, abstractmethod
from typing import List

class Notification(ABC):
    def __init__(self, recipients: List[str] = None):
        self.recipients = recipients if recipients else []

    def add_recipient(self, recipient: str):
        self.recipients.append(recipient)

    @abstractmethod
    def send(self, message: str):
        pass

class TerminalNotification(Notification):
    def __init__(self):
        super().__init__(recipients=None)

    def send(self, message: str):
        self._send_message(message)

    def _send_message(self, message: str):
        print(f"Notification: {message}")

class EmailNotification(Notification):
    def send(self, message: str):
        for recipient in self.recipients:
            self._send_message(recipient, message)

    def _send_message(self, recipient: str, message: str):
        # TODO: Implement actual email sending logic.
        print(f"Email sent to {recipient}: {message}")
