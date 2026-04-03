from typing import List
from database.connection import DatabaseConnection
from database.models import Invoice, InvoiceItem


class InvoiceRepository:
    """Repository for invoice persistence"""

    @staticmethod
    def add(invoice: Invoice) -> None:
        """Add a new invoice"""
        query = """
            INSERT INTO invoices (id, closing_day, due_day, status, total, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            invoice.id,
            invoice.closing_day,
            invoice.due_day,
            invoice.status,
            invoice.total,
            invoice.created_at,
        )

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

    @staticmethod
    def get_all() -> List[Invoice]:
        """Retrieve all invoices"""
        query = """
            SELECT id, closing_day, due_day, status, total, created_at FROM invoices
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            Invoice(
                id=row[0],
                closing_day=row[1],
                due_day=row[2],
                status=row[3],
                total=row[4],
                created_at=row[5],
            )
            for row in rows
        ]

    @staticmethod
    def get_by_id(invoice_id: str) -> Invoice | None:
        """Retrieve an invoice by ID"""
        query = """
            SELECT id, closing_day, due_day, status, total, created_at FROM invoices WHERE id = ?
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (invoice_id,))
            row = cursor.fetchone()

        if row:
            return Invoice(
                id=row[0],
                closing_day=row[1],
                due_day=row[2],
                status=row[3],
                total=row[4],
                created_at=row[5],
            )
        return None

    @staticmethod
    def get_open() -> Invoice | None:
        """Retrieve the current open invoice"""
        query = """
            SELECT id, closing_day, due_day, status, total, created_at FROM invoices
            WHERE status = 'open' ORDER BY created_at DESC LIMIT 1
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()

        if row:
            return Invoice(
                id=row[0],
                closing_day=row[1],
                due_day=row[2],
                status=row[3],
                total=row[4],
                created_at=row[5],
            )
        return None

    @staticmethod
    def update_status(invoice_id: str, status: str) -> None:
        """Update invoice status"""
        query = "UPDATE invoices SET status = ? WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (status, invoice_id))

    @staticmethod
    def update_total(invoice_id: str, total: float) -> None:
        """Update invoice total"""
        query = "UPDATE invoices SET total = ? WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (total, invoice_id))

    @staticmethod
    def delete(invoice_id: str) -> None:
        """Delete an invoice (and its items via cascade)"""
        query = "DELETE FROM invoices WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (invoice_id,))


class InvoiceItemRepository:
    """Repository for invoice items persistence"""

    @staticmethod
    def add(item: InvoiceItem) -> None:
        """Add an item to an invoice"""
        query = """
            INSERT INTO invoice_items (id, invoice_id, amount, category, date)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (item.id, item.invoice_id, item.amount, item.category, item.date)

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

    @staticmethod
    def get_by_invoice(invoice_id: str) -> List[InvoiceItem]:
        """Retrieve all items for an invoice"""
        query = """
            SELECT id, invoice_id, amount, category, date FROM invoice_items
            WHERE invoice_id = ?
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (invoice_id,))
            rows = cursor.fetchall()

        return [
            InvoiceItem(id=row[0], invoice_id=row[1], amount=row[2], category=row[3], date=row[4])
            for row in rows
        ]

    @staticmethod
    def delete_by_invoice(invoice_id: str) -> None:
        """Delete all items for an invoice"""
        query = "DELETE FROM invoice_items WHERE invoice_id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (invoice_id,))

    @staticmethod
    def get_total_for_invoice(invoice_id: str) -> float:
        """Calculate total amount for an invoice"""
        query = "SELECT SUM(amount) FROM invoice_items WHERE invoice_id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (invoice_id,))
            result = cursor.fetchone()

        return result[0] if result and result[0] else 0.0
