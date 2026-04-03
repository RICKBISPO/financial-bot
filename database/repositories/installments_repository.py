from typing import List
from database.connection import DatabaseConnection
from database.models import Installment


class InstallmentRepository:
    """Repository for installment persistence"""

    @staticmethod
    def add(installment: Installment) -> None:
        """Add a new installment"""
        query = """
            INSERT INTO installments
            (id, amount, category, total_installments, paid_installments, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            installment.id,
            installment.amount,
            installment.category,
            installment.total_installments,
            installment.paid_installments,
            installment.created_date,
        )

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

    @staticmethod
    def get_all() -> List[Installment]:
        """Retrieve all installments"""
        query = """
            SELECT id, amount, category, total_installments, paid_installments, created_date
            FROM installments
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            Installment(
                id=row[0],
                amount=row[1],
                category=row[2],
                total_installments=row[3],
                paid_installments=row[4],
                created_date=row[5],
            )
            for row in rows
        ]

    @staticmethod
    def get_by_id(installment_id: str) -> Installment | None:
        """Retrieve an installment by ID"""
        query = """
            SELECT id, amount, category, total_installments, paid_installments, created_date
            FROM installments WHERE id = ?
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (installment_id,))
            row = cursor.fetchone()

        if row:
            return Installment(
                id=row[0],
                amount=row[1],
                category=row[2],
                total_installments=row[3],
                paid_installments=row[4],
                created_date=row[5],
            )
        return None

    @staticmethod
    def increment_paid(installment_id: str) -> None:
        """Increment paid installments count"""
        query = """
            UPDATE installments SET paid_installments = paid_installments + 1
            WHERE id = ?
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (installment_id,))

    @staticmethod
    def delete(installment_id: str) -> None:
        """Delete an installment"""
        query = "DELETE FROM installments WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (installment_id,))
