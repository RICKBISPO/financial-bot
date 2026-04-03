from dataclasses import dataclass


@dataclass
class Installment:
    """Represents an installment plan (e.g., 12x paid items)"""

    id: str
    amount: float
    category: str
    total_installments: int
    paid_installments: int
    created_date: str  # ISO format

    def __hash__(self):
        return hash(self.id)

    @property
    def remaining_installments(self) -> int:
        return self.total_installments - self.paid_installments

    @property
    def per_installment_value(self) -> float:
        return self.amount / self.total_installments
