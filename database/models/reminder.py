from dataclasses import dataclass
from typing import Literal


@dataclass
class Reminder:
    """Represents a reminder for events"""

    id: str
    type: Literal["fixed", "installment", "standalone"]
    linked_id: str
    days_before: int
    message: str
    created_date: str  # ISO format

    def __hash__(self):
        return hash(self.id)
