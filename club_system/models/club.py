# models/club.py
import uuid
from dataclasses import dataclass, field
from typing import List
from models.employee import Employee


@dataclass
class Club:
    name: str
    funds: float
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


@dataclass
class Player(Employee):
    specialty: str = None
    ability: int = 70  # 初始能力值