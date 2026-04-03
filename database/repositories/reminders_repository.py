from typing import List
from database.connection import DatabaseConnection
from database.models import Reminder


class ReminderRepository:
    """Repository for reminder persistence"""

    @staticmethod
    def add(reminder: Reminder) -> None:
        """Add a new reminder"""
        query = """
            INSERT INTO reminders (id, type, linked_id, days_before, message, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            reminder.id,
            reminder.type,
            reminder.linked_id,
            reminder.days_before,
            reminder.message,
            reminder.created_date,
        )

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

    @staticmethod
    def get_all() -> List[Reminder]:
        """Retrieve all reminders"""
        query = """
            SELECT id, type, linked_id, days_before, message, created_date FROM reminders
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            Reminder(
                id=row[0],
                type=row[1],
                linked_id=row[2],
                days_before=row[3],
                message=row[4],
                created_date=row[5],
            )
            for row in rows
        ]

    @staticmethod
    def get_by_id(reminder_id: str) -> Reminder | None:
        """Retrieve a reminder by ID"""
        query = """
            SELECT id, type, linked_id, days_before, message, created_date
            FROM reminders WHERE id = ?
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (reminder_id,))
            row = cursor.fetchone()

        if row:
            return Reminder(
                id=row[0],
                type=row[1],
                linked_id=row[2],
                days_before=row[3],
                message=row[4],
                created_date=row[5],
            )
        return None

    @staticmethod
    def delete(reminder_id: str) -> None:
        """Delete a reminder"""
        query = "DELETE FROM reminders WHERE id = ?"

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (reminder_id,))

    @staticmethod
    def get_by_linked_id(linked_id: str) -> List[Reminder]:
        """Get all reminders linked to a specific entity"""
        query = """
            SELECT id, type, linked_id, days_before, message, created_date
            FROM reminders WHERE linked_id = ?
        """

        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (linked_id,))
            rows = cursor.fetchall()

        return [
            Reminder(
                id=row[0],
                type=row[1],
                linked_id=row[2],
                days_before=row[3],
                message=row[4],
                created_date=row[5],
            )
            for row in rows
        ]
