from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Role(Enum):
    DIRECTOR = "director"
    COACH = "coach"
    PLAYER = "player"
    STAFF = "staff"
    GOALKEEPER = "goalkeeper"
    DEFENDER = "defender"
    MIDFIELDER = "midfielder"
    STRIKER = "striker"

@dataclass
class Employee:
    eid: str
    name: str
    salary: float
    role: Role
    join_date: str  # 格式：YYYY-MM-DD
    contract_end: Optional[str] = None

@dataclass
class Player(Employee):
    ability: int = 70
    specialty: str = "无"
    injured: bool = False
    position: Optional[str] = None

@dataclass
class Coach(Employee):
    license_level: int = 1
    training_style: str = "平衡"

@dataclass
class Goalkeeper(Player):
    reflexes: int = 80
    positioning: int = 75

@dataclass
class Defender(Player):
    tackling: int = 85
    heading: int = 80

@dataclass
class Midfielder(Player):
    passing: int = 88
    stamina: int = 90

@dataclass
class Striker(Player):
    finishing: int = 90
    speed: int = 85