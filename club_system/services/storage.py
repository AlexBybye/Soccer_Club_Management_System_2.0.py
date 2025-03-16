import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from models.user import User


class UserStorage:
    USER_DATA_PATH = Path("data/users.json")

    @classmethod
    def _ensure_data_file(cls):
        """确保数据文件存在"""
        cls.USER_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not cls.USER_DATA_PATH.exists():
            cls.USER_DATA_PATH.write_text('{"users": {}}')

    @classmethod
    def save_user(cls, user: User):
        """保存用户数据（处理Optional字段）"""
        cls._ensure_data_file()
        data = json.loads(cls.USER_DATA_PATH.read_text())
        data["users"][user.username] = user.to_dict()
        cls.USER_DATA_PATH.write_text(json.dumps(data, indent=2))

    @classmethod
    def get_user(cls, username: str) -> Optional[User]:
        """获取用户（返回Optional类型）"""
        cls._ensure_data_file()
        data = json.loads(cls.USER_DATA_PATH.read_text())
        user_data = data["users"].get(username)
        return User.from_dict(user_data) if user_data else None

    @classmethod
    def update_optional_fields(cls, username: str, **kwargs):
        """更新可选字段接口"""
        user = cls.get_user(username)
        if not user:
            raise ValueError("用户不存在")

        for field, value in kwargs.items():
            if hasattr(user, field):
                setattr(user, field, value)

        cls.save_user(user)