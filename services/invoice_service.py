import uuid
from datetime import datetime
from typing import List

from database.models import Invoice, InvoiceItem
from database.repositories import InvoiceRepository, InvoiceItemRepository
from database.repositories import BalanceRepository


class InvoiceService:
    """Service layer for invoice (credit card) operations"""

    @staticmethod
    def create_or_get_open_invoice() -> Invoice:
        """Get or create the current open invoice"""
        open_invoice = InvoiceRepository.get_open()

        if open_invoice:
            return open_invoice

        # Create new invoice
        invoice = Invoice(
            id=str(uuid.uuid4()),
            closing_day=5,
            due_day=12,
            status="open",
            total=0.0,
            created_at=datetime.now().isoformat(),
        )

        InvoiceRepository.add(invoice)
        return invoice

    @staticmethod
    def add_item_to_invoice(invoice_id: str, amount: float, category: str) -> InvoiceItem:
        """Add an item to an invoice"""
        invoice = InvoiceRepository.get_by_id(invoice_id)

        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        # Create item
        item = InvoiceItem(
            id=str(uuid.uuid4()),
            invoice_id=invoice_id,
            amount=amount,
            category=category,
            date=datetime.now().isoformat(),
        )

        InvoiceItemRepository.add(item)

        # Update invoice total
        new_total = InvoiceItemRepository.get_total_for_invoice(invoice_id)
        InvoiceRepository.update_total(invoice_id, new_total)

        return item

    @staticmethod
    def add_credit_transaction(amount: float, category: str) -> InvoiceItem:
        """Record a credit transaction (goes to open invoice)"""
        invoice = InvoiceService.create_or_get_open_invoice()
        return InvoiceService.add_item_to_invoice(invoice.id, amount, category)

    @staticmethod
    def get_open_invoice() -> Invoice | None:
        """Retrieve the current open invoice"""
        return InvoiceRepository.get_open()

    @staticmethod
    def get_invoice_items(invoice_id: str) -> List[InvoiceItem]:
        """Get all items for an invoice"""
        return InvoiceItemRepository.get_by_invoice(invoice_id)

    @staticmethod
    def close_invoice(invoice_id: str) -> None:
        """Close an invoice (ready to be paid)"""
        invoice = InvoiceRepository.get_by_id(invoice_id)

        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        InvoiceRepository.update_status(invoice_id, "closed")

    @staticmethod
    def pay_invoice(invoice_id: str) -> None:
        """Pay an invoice using available balance"""
        invoice = InvoiceRepository.get_by_id(invoice_id)

        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        balance = BalanceRepository.get_current()

        if balance.amount < invoice.total:
            raise ValueError(
                f"Insufficient balance to pay invoice. "
                f"Balance: {balance.amount}, Invoice: {invoice.total}"
            )

        # Deduct from balance and mark as paid
        BalanceRepository.subtract(invoice.total)
        InvoiceRepository.update_status(invoice_id, "paid")

    @staticmethod
    def get_all_invoices() -> List[Invoice]:
        """Retrieve all invoices"""
        return InvoiceRepository.get_all()

    @staticmethod
    def delete_invoice(invoice_id: str) -> None:
        """Delete an invoice and its items"""
        invoice = InvoiceRepository.get_by_id(invoice_id)

        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        InvoiceItemRepository.delete_by_invoice(invoice_id)
        InvoiceRepository.delete(invoice_id)
