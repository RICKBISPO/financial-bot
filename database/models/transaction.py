from dataclasses import dataclass
from typing import Literal


@dataclass
class Transaction:
    """Represents a financial transaction (debit, credit, or income)"""

    id: str
    type: Literal["debit", "credit", "entry"]
    amount: float
    category: str
    date: str  # ISO format

    def __hash__(self):
        return hash(self.id)
