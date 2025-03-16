import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from club_system.models.club import Club
from club_system.models.user import User
from club_system.models.employee import Employee, Player

class UserStorage:
    USER_DATA_PATH = Path("data/users.json")

    @classmethod
    def _ensure_data_file(cls):
        """确保数据文件存在"""
        cls.USER_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not cls.USER_DATA_PATH.exists():
            cls.USER_DATA_PATH.write_text('{"users": {}}')

    @classmethod
    def update_user(cls, user: User):
        """更新用户数据"""
        cls._ensure_data_file()
        data = json.loads(cls.USER_DATA_PATH.read_text())
        data["users"][user.username] = user.to_dict()
        cls.USER_DATA_PATH.write_text(json.dumps(data, indent=2))

    @classmethod
    def user_exists(cls, username: str) -> bool:
        """检查用户是否已存在"""
        cls._ensure_data_file()
        data = json.loads(cls.USER_DATA_PATH.read_text())
        return username in data["users"]

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


class ClubStorage:
    CLUB_DATA_PATH = Path("data/clubs.json")

    @classmethod
    def _ensure_data_file(cls):
        """确保数据文件存在"""
        cls.CLUB_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not cls.CLUB_DATA_PATH.exists():
            cls.CLUB_DATA_PATH.write_text('{"clubs": {}}')

    @classmethod
    def save(cls, club: Club):
        """保存俱乐部数据"""
        cls._ensure_data_file()
        data = json.loads(cls.CLUB_DATA_PATH.read_text())
        data["clubs"][club.name] = {
            "name": club.name,
            "funds": club.funds,
            "establish_date": club.establish_date,
            "director_key": club.director_key,
            "employees": [
                {
                    **vars(emp),
                    "role": emp.role.value  # 将枚举转换为字符串
                } for emp in club.employees
            ]
        }
        cls.CLUB_DATA_PATH.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, name: str) -> Optional[Club]:
        """加载俱乐部数据"""
        cls._ensure_data_file()
        data = json.loads(cls.CLUB_DATA_PATH.read_text())
        club_data = data["clubs"].get(name)

        if not club_data:
            return None

        # 从字符串重新创建 Role 枚举
        from club_system.models.employee import Role

        club = Club(
            name=club_data['name'],
            funds=club_data['funds'],
            establish_date=club_data.get('establish_date', datetime.now().strftime("%Y-%m-%d")),
            director_key=club_data['director_key']
        )

        for emp_data in club_data.get('employees', []):
            # 从字符串重新创建 Role 枚举
            emp_data['role'] = Role(emp_data['role'])

            if emp_data.get('specialty'):
                emp = Player(**emp_data)
            else:
                emp = Employee(**emp_data)
            club.add_employee(emp)

        return club
