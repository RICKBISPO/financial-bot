from dataclasses import dataclass


@dataclass
class InvoiceItem:
    """Represents a single item in an invoice"""

    id: str
    invoice_id: str
    amount: float
    category: str
    date: str  # ISO format

    def __hash__(self):
        return hash(self.id)
