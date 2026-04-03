from dataclasses import dataclass


@dataclass
class Balance:
    """Represents the current balance"""

    id: int
    amount: float

    def __hash__(self):
        return hash(self.id)
