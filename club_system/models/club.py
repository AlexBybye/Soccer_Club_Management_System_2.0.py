import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import List
from .employee import Employee


@dataclass
class Club:
    name: str
    funds: float
    establish_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    employees: List[Employee] = field(default_factory=list)
    director_key: str = field(default_factory=lambda: uuid.uuid4().hex)
    def add_employee(self, employee: Employee):
        self.employees.append(employee)


# models/employee.py
from dataclasses import dataclass
from enum import Enum


class Role(Enum):
    DIRECTOR = "director"
    COACH = "coach"
    PLAYER = "player"


@dataclass
class Employee:
    eid: str
    name: str
    salary: float
    role: Role
    join_date: str = ''  # 添加 join_date 参数

@dataclass
class Player(Employee):
    specialty: str = None
    ability: int = 70  # 初始能力值
    injured: bool = False  # 添加伤病状态