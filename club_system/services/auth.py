from club_system.models.user import User, UserRole
from club_system.services.storage import UserStorage
from club_system.utils.security import (
    hash_password,
    verify_password,
    generate_password_reset_token
)


class AuthSystem:
    MAX_FAILED_ATTEMPTS = 5

    def __init__(self):
        self.current_user = None

    def register_user(self, username: str, password: str, role: UserRole, club_id: str) -> User:
        """用户注册流程"""
        if UserStorage.user_exists(username):
            raise ValueError("用户名已存在")

        if len(password) < 8:
            raise ValueError("密码长度需至少8个字符")

        return UserStorage.save_user(
            User(
                username=username,
                password_hash=hash_password(password),
                club_id=club_id,
                role=role
            )
        )

    def login(self, username: str, password: str) -> bool:
        """安全登录流程"""
        user = UserStorage.get_user(username)
        if not user:
            return False

        if user.is_locked:
            raise AccountLockedError("账户已锁定，请联系管理员")

        if verify_password(password, user.password_hash):
            user.failed_attempts = 0
            self.current_user = user
            UserStorage.update_user(user)
            return True
        else:
            user.failed_attempts += 1
            if user.failed_attempts >= self.MAX_FAILED_ATTEMPTS:
                user.is_locked = True
            UserStorage.update_user(user)
            return False

    def initiate_password_reset(self, username: str) -> str:
        """密码重置流程"""
        user = UserStorage.get_user(username)
        if not user:
            raise ValueError("用户不存在")

        reset_token = generate_password_reset_token()
        user.password_reset_token = hash_password(reset_token)
        UserStorage.update_user(user)
        return reset_token


class AccountLockedError(Exception):
    """自定义账户锁定异常"""
    pass