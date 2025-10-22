from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from abc import abstractmethod


@dataclass
class UsageHistory:
    user: str
    taken_at: datetime
    released_at: datetime
    stolen_by: str = None
    was_stolen: bool = False

@abstractmethod
class Resource:
    def __init__(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        self.name = name
        self.metadata = metadata or {}
        self.taken_by: Optional[str] = None
        self.taken_at: Optional[datetime] = None
        self.history: List[UsageHistory] = []

    def is_taken(self) -> bool:
        return self.taken_by is not None

    def try_to_take(self, user: str) -> bool:
        if self.is_taken():
            return False
        self.taken_by = user
        self.taken_at = datetime.now()
        return True

    def steal(self, user: str) -> Dict[str, Any]:
        previous_holder = self.taken_by
        previous_taken_at = self.taken_at
        if previous_holder:
            self.history.append(UsageHistory(
                user=previous_holder,
                taken_at=previous_taken_at,
                released_at=datetime.now(),
                was_stolen=True,
                stolen_by=user
            ))
        self.taken_by = user
        self.taken_at = datetime.now()
        return {
            "previous_holder": previous_holder,
            "previous_taken_at": previous_taken_at,
        }

    def release(self, user: Optional[str] = None) -> bool:
        if not self.is_taken():
            return False
        if user is not None and user != self.taken_by:
            return False
        self.history.append(UsageHistory(
            user=self.taken_by,
            taken_at=self.taken_at,
            released_at=datetime.now(),
        ))
        self.taken_by = None
        self.taken_at = None
        return True

    def force_release(self) -> bool:
        return self.release() if self.is_taken() else False

    def get_current_holder(self) -> Optional[str]:
        return self.taken_by

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_taken": self.is_taken(),
            "taken_by": self.taken_by,
            "taken_at": self.taken_at.isoformat() if self.taken_at else None,
        }

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_taken": self.is_taken(),
            "taken_by": self.taken_by,
            "taken_at": self.taken_at.isoformat() if self.taken_at else None,
            "metadata": self.metadata
        }

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        history_list = []
        for entry in reversed(self.history[-limit:] if limit else self.history):
            history_list.append({
                "user": entry.user,
                "taken_at": entry.taken_at.isoformat(),
                "released_at": entry.released_at.isoformat() if entry.released_at else None,
                "was_stolen": entry.was_stolen,
            })

        return history_list
