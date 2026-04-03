from dataclasses import dataclass, field
from typing import Literal, List


@dataclass
class Invoice:
    """Represents a credit card invoice"""

    id: str
    closing_day: int
    due_day: int
    status: Literal["open", "closed", "paid"]
    total: float
    created_at: str  # ISO format
    items: List = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

    @property
    def is_open(self) -> bool:
        return self.status == "open"

    @property
    def is_paid(self) -> bool:
        return self.status == "paid"
