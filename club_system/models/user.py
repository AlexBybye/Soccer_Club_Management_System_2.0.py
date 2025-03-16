from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional

class UserRole(Enum):
    DIRECTOR = "director"
    COACH = "coach"
    PLAYER = "player"
    STAFF = "staff"

@dataclass
class User:
    username: str
    password_hash: str
    club_id: str
    role: UserRole
    last_login: Optional[datetime] = field(default=None)
    failed_attempts: int = field(default=0)
    password_reset_token: Optional[str] = field(default=None)
    is_locked: bool = field(default=False)

    def to_dict(self) -> dict:
        """转换为字典格式（含Optional字段处理）"""
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "club_id": self.club_id,
            "role": self.role.value,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "failed_attempts": self.failed_attempts,
            "password_reset_token": self.password_reset_token,
            "is_locked": self.is_locked
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """从字典创建实例（含Optional字段处理）"""
        return cls(
            username=data["username"],
            password_hash=data["password_hash"],
            club_id=data["club_id"],
            role=UserRole(data["role"]),
            last_login=datetime.fromisoformat(data["last_login"]) if data["last_login"] else None,
            failed_attempts=data.get("failed_attempts", 0),
            password_reset_token=data.get("password_reset_token"),
            is_locked=data.get("is_locked", False)
        )