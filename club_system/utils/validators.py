from datetime import datetime
from typing import Optional

class UserValidator:
    @staticmethod
    def validate_last_login(value: Optional[str]) -> Optional[datetime]:
        """验证可选时间字段"""
        if value is None:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("无效的时间格式，应使用ISO格式")

    @staticmethod
    def validate_reset_token(token: Optional[str]) -> bool:
        """验证可选重置令牌"""
        if token is None:
            return True
        return len(token) >= 16  # 示例验证逻辑

    @staticmethod
    def validate_lock_status(is_locked: bool, failed_attempts: int) -> bool:
        """验证账户锁定状态逻辑"""
        if failed_attempts >= 5 and not is_locked:
            return False  # 异常状态
        return True