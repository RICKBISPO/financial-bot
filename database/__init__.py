from database.connection import DatabaseConnection
from database.init_db import init_database
from database.models import (
    Transaction,
    Balance,
    FixedExpense,
    Installment,
    Invoice,
    InvoiceItem,
    Reminder,
)
from database.repositories.transactions_repository import TransactionRepository
from database.repositories.balance_repository import BalanceRepository
from database.repositories.fixed_expenses_repository import FixedExpenseRepository
from database.repositories.installments_repository import InstallmentRepository
from database.repositories.invoices_repository import InvoiceRepository, InvoiceItemRepository
from database.repositories.reminders_repository import ReminderRepository


# Transaction functions
def add_transaction(transaction: Transaction) -> None:
    """Add a new transaction"""
    TransactionRepository.add(transaction)


def get_transactions() -> list[Transaction]:
    """Get all transactions"""
    return TransactionRepository.get_all()


def delete_transaction(transaction_id: str) -> None:
    """Delete a transaction"""
    TransactionRepository.delete(transaction_id)


# Balance functions
def get_balance() -> float:
    """Get current balance"""
    balance = BalanceRepository.get_current()
    return balance.amount


def update_balance(amount: float) -> None:
    """Update balance to a specific value"""
    BalanceRepository.update(amount)


# Fixed Expense functions (fixo)
def add_fixo(fixed_expense: FixedExpense) -> None:
    """Add a new fixed expense"""
    FixedExpenseRepository.add(fixed_expense)


def get_fixos() -> list[FixedExpense]:
    """Get all fixed expenses"""
    return FixedExpenseRepository.get_all()


def delete_fixo(fixed_id: str) -> None:
    """Delete a fixed expense"""
    FixedExpenseRepository.delete(fixed_id)


# Installment functions (parcelado)
def add_parcelado(installment: Installment) -> None:
    """Add a new installment"""
    InstallmentRepository.add(installment)


def get_parcelados() -> list[Installment]:
    """Get all installments"""
    return InstallmentRepository.get_all()


def delete_parcelado(installment_id: str) -> None:
    """Delete an installment"""
    InstallmentRepository.delete(installment_id)


# Invoice functions (fatura)
def add_to_fatura(item: InvoiceItem) -> None:
    """Add an item to invoice"""
    InvoiceItemRepository.add(item)


def get_fatura_aberta() -> Invoice | None:
    """Get the open invoice"""
    return InvoiceRepository.get_open()


def get_fatura_items(invoice_id: str) -> list[InvoiceItem]:
    """Get all items for an invoice"""
    return InvoiceItemRepository.get_by_invoice(invoice_id)


def create_or_get_fatura(invoice: Invoice) -> Invoice:
    """Create or get an invoice"""
    existing = InvoiceRepository.get_open()
    if existing:
        return existing
    InvoiceRepository.add(invoice)
    return invoice


def close_fatura(invoice_id: str) -> None:
    """Close an invoice"""
    InvoiceRepository.update_status(invoice_id, "closed")


def pay_fatura(invoice_id: str) -> None:
    """Mark an invoice as paid"""
    InvoiceRepository.update_status(invoice_id, "paid")


__all__ = [
    "DatabaseConnection",
    "init_database",
    "Transaction",
    "Balance",
    "FixedExpense",
    "Installment",
    "Invoice",
    "InvoiceItem",
    "Reminder",
    "add_transaction",
    "get_transactions",
    "delete_transaction",
    "get_balance",
    "update_balance",
    "add_fixo",
    "get_fixos",
    "delete_fixo",
    "add_parcelado",
    "get_parcelados",
    "delete_parcelado",
    "add_to_fatura",
    "get_fatura_aberta",
    "get_fatura_items",
    "create_or_get_fatura",
    "close_fatura",
    "pay_fatura",
]
