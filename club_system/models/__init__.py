"""
数据模型模块
"""
from __future__ import annotations
from typing import Optional
from datetime import datetime

# 导出俱乐部相关模型
from .club import Club

# 导出员工相关模型
from .employee import (
    Role,
    Employee,
    Player,
    Coach,
    Goalkeeper,
    Defender,
    Midfielder,
    Striker
)

# 导出用户相关模型
from .user import User, UserRole

__all__ = [
    # 俱乐部模型
    'Club',

    # 员工模型
    'Role', 'Employee', 'Player', 'Coach',
    'Goalkeeper', 'Defender', 'Midfielder', 'Striker',

    # 用户模型
    'User', 'UserRole',

    # 公共类型
    'Optional', 'datetime'
]