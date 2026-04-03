from typing import List
from database.connection import DatabaseConnection
from database.models import Transaction


class TransactionRepository:
    """Repository for transaction persistence"""

    @staticmethod
    def add(transaction: Transaction) -> None:
        """Add a new transaction"""
        query = """
            INSERT INTO transactions (id, type, amount, category, date)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            transaction.id,
            transaction.type,
            transaction.amount,
            transaction.category,
            transaction.date,
        )

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

    @staticmethod
    def get_all() -> List[Transaction]:
        """Retrieve all transactions"""
        query = "SELECT id, type, amount, category, date FROM transactions"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            Transaction(id=row[0], type=row[1], amount=row[2], category=row[3], date=row[4])
            for row in rows
        ]

    @staticmethod
    def get_by_id(transaction_id: str) -> Transaction | None:
        """Retrieve a transaction by ID"""
        query = "SELECT id, type, amount, category, date FROM transactions WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (transaction_id,))
            row = cursor.fetchone()

        if row:
            return Transaction(
                id=row[0], type=row[1], amount=row[2], category=row[3], date=row[4]
            )
        return None

    @staticmethod
    def delete(transaction_id: str) -> None:
        """Delete a transaction"""
        query = "DELETE FROM transactions WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (transaction_id,))

    @staticmethod
    def get_latest(limit: int = 10) -> List[Transaction]:
        """Get latest N transactions"""
        query = """
            SELECT id, type, amount, category, date FROM transactions
            ORDER BY date DESC LIMIT ?
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

        return [
            Transaction(id=row[0], type=row[1], amount=row[2], category=row[3], date=row[4])
            for row in rows
        ]
