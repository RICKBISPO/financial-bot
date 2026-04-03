import uuid
from datetime import datetime
from typing import List

from database.models import Transaction, FixedExpense, Installment, Balance
from database.repositories import (
    TransactionRepository,
    BalanceRepository,
    FixedExpenseRepository,
    InstallmentRepository,
)


class FinanceService:
    """Service layer for financial operations"""

    # Transaction operations
    @staticmethod
    def create_expense(
        amount: float, category: str, transaction_type: str = "debit"
    ) -> Transaction:
        """Create and record a new expense (debit or credit)"""
        transaction = Transaction(
            id=str(uuid.uuid4()),
            type=transaction_type,
            amount=amount,
            category=category,
            date=datetime.now().isoformat(),
        )

        TransactionRepository.add(transaction)

        # Update balance only for debits
        if transaction_type == "debit":
            BalanceRepository.subtract(amount)

        return transaction

    @staticmethod
    def record_income(amount: float, category: str) -> Transaction:
        """Record an income entry"""
        transaction = Transaction(
            id=str(uuid.uuid4()),
            type="entry",
            amount=amount,
            category=category,
            date=datetime.now().isoformat(),
        )

        TransactionRepository.add(transaction)
        BalanceRepository.add(amount)

        return transaction

    @staticmethod
    def get_all_transactions() -> List[Transaction]:
        """Retrieve all transactions"""
        return TransactionRepository.get_all()

    @staticmethod
    def get_latest_transactions(limit: int = 10) -> List[Transaction]:
        """Get latest N transactions"""
        return TransactionRepository.get_latest(limit)

    @staticmethod
    def delete_transaction(transaction_id: str) -> None:
        """Delete a transaction and reverse its balance effect"""
        transaction = TransactionRepository.get_by_id(transaction_id)

        if not transaction:
            raise ValueError(f"Transaction {transaction_id} not found")

        # Reverse balance effect
        if transaction.type == "debit":
            BalanceRepository.add(transaction.amount)
        elif transaction.type == "entry":
            BalanceRepository.subtract(transaction.amount)

        TransactionRepository.delete(transaction_id)

    # Balance operations
    @staticmethod
    def get_balance() -> Balance:
        """Get current balance"""
        return BalanceRepository.get_current()

    # Fixed expense operations
    @staticmethod
    def create_fixed_expense(amount: float, category: str) -> FixedExpense:
        """Create a recurring monthly expense"""
        fixed = FixedExpense(
            id=str(uuid.uuid4()),
            amount=amount,
            category=category,
            created_date=datetime.now().isoformat(),
        )

        FixedExpenseRepository.add(fixed)
        return fixed

    @staticmethod
    def get_all_fixed_expenses() -> List[FixedExpense]:
        """Retrieve all fixed expenses"""
        return FixedExpenseRepository.get_all()

    @staticmethod
    def delete_fixed_expense(fixed_id: str) -> None:
        """Delete a fixed expense"""
        fixed = FixedExpenseRepository.get_by_id(fixed_id)

        if not fixed:
            raise ValueError(f"Fixed expense {fixed_id} not found")

        FixedExpenseRepository.delete(fixed_id)

    # Installment operations
    @staticmethod
    def create_installment(
        amount: float, category: str, total_installments: int
    ) -> Installment:
        """Create an installment plan"""
        installment = Installment(
            id=str(uuid.uuid4()),
            amount=amount,
            category=category,
            total_installments=total_installments,
            paid_installments=0,
            created_date=datetime.now().isoformat(),
        )

        InstallmentRepository.add(installment)
        return installment

    @staticmethod
    def get_all_installments() -> List[Installment]:
        """Retrieve all installments"""
        return InstallmentRepository.get_all()

    @staticmethod
    def delete_installment(installment_id: str) -> None:
        """Delete an installment plan"""
        installment = InstallmentRepository.get_by_id(installment_id)

        if not installment:
            raise ValueError(f"Installment {installment_id} not found")

        InstallmentRepository.delete(installment_id)

    @staticmethod
    def increment_installment_payment(installment_id: str) -> None:
        """Mark an installment as paid"""
        installment = InstallmentRepository.get_by_id(installment_id)

        if not installment:
            raise ValueError(f"Installment {installment_id} not found")

        InstallmentRepository.increment_paid(installment_id)
