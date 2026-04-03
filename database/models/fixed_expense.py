from dataclasses import dataclass


@dataclass
class FixedExpense:
    """Represents a monthly recurring expense"""

    id: str
    amount: float
    category: str
    created_date: str  # ISO format

    def __hash__(self):
        return hash(self.id)
