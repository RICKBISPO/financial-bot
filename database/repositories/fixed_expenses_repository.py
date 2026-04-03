from typing import List
from database.connection import DatabaseConnection
from database.models import FixedExpense


class FixedExpenseRepository:
    """Repository for fixed expense persistence"""

    @staticmethod
    def add(fixed_expense: FixedExpense) -> None:
        """Add a new fixed expense"""
        query = """
            INSERT INTO fixed_expenses (id, amount, category, created_date)
            VALUES (?, ?, ?, ?)
        """
        params = (
            fixed_expense.id,
            fixed_expense.amount,
            fixed_expense.category,
            fixed_expense.created_date,
        )

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

    @staticmethod
    def get_all() -> List[FixedExpense]:
        """Retrieve all fixed expenses"""
        query = "SELECT id, amount, category, created_date FROM fixed_expenses"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            FixedExpense(id=row[0], amount=row[1], category=row[2], created_date=row[3])
            for row in rows
        ]

    @staticmethod
    def get_by_id(fixed_id: str) -> FixedExpense | None:
        """Retrieve a fixed expense by ID"""
        query = "SELECT id, amount, category, created_date FROM fixed_expenses WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (fixed_id,))
            row = cursor.fetchone()

        if row:
            return FixedExpense(id=row[0], amount=row[1], category=row[2], created_date=row[3])
        return None

    @staticmethod
    def delete(fixed_id: str) -> None:
        """Delete a fixed expense"""
        query = "DELETE FROM fixed_expenses WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (fixed_id,))
