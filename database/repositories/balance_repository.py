from database.connection import DatabaseConnection
from database.models import Balance


class BalanceRepository:
    """Repository for balance persistence"""

    @staticmethod
    def get_current() -> Balance:
        """Retrieve current balance"""
        query = "SELECT id, amount FROM balance LIMIT 1"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()

        if row:
            return Balance(id=row[0], amount=row[1])

        # Create default balance if not exists
        return Balance(id=1, amount=0.0)

    @staticmethod
    def update(amount: float) -> None:
        """Update balance value"""
        query = "UPDATE balance SET amount = ? WHERE id = 1"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (amount,))

    @staticmethod
    def add(amount: float) -> None:
        """Add to current balance"""
        current = BalanceRepository.get_current()
        BalanceRepository.update(current.amount + amount)

    @staticmethod
    def subtract(amount: float) -> None:
        """Subtract from current balance"""
        current = BalanceRepository.get_current()
        BalanceRepository.update(current.amount - amount)
