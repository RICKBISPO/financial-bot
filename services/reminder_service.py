import uuid
from datetime import datetime
from typing import List, Literal

from database.models import Reminder
from database.repositories import ReminderRepository


class ReminderService:
    """Service layer for reminder operations"""

    @staticmethod
    def create_reminder(
        reminder_type: Literal["fixed", "installment", "standalone"],
        linked_id: str,
        days_before: int,
        message: str = "",
    ) -> Reminder:
        """Create a new reminder"""
        reminder = Reminder(
            id=str(uuid.uuid4()),
            type=reminder_type,
            linked_id=linked_id,
            days_before=days_before,
            message=message,
            created_date=datetime.now().isoformat(),
        )

        ReminderRepository.add(reminder)
        return reminder

    @staticmethod
    def get_all_reminders() -> List[Reminder]:
        """Retrieve all reminders"""
        return ReminderRepository.get_all()

    @staticmethod
    def get_reminders_for_entity(linked_id: str) -> List[Reminder]:
        """Get all reminders linked to a specific entity"""
        return ReminderRepository.get_by_linked_id(linked_id)

    @staticmethod
    def delete_reminder(reminder_id: str) -> None:
        """Delete a reminder"""
        reminder = ReminderRepository.get_by_id(reminder_id)

        if not reminder:
            raise ValueError(f"Reminder {reminder_id} not found")

        ReminderRepository.delete(reminder_id)

    @staticmethod
    def delete_reminders_for_entity(linked_id: str) -> None:
        """Delete all reminders for an entity"""
        reminders = ReminderRepository.get_by_linked_id(linked_id)

        for reminder in reminders:
            ReminderRepository.delete(reminder.id)
