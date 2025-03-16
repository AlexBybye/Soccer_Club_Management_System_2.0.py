import bcrypt
import secrets
from typing import Optional

def generate_secure_key(length: int = 16) -> str:
    """生成加密安全的随机密钥"""
    return secrets.token_urlsafe(length)

def hash_password(password: str) -> str:
    """使用bcrypt进行密码哈希"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码与哈希是否匹配"""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except (ValueError, TypeError):
        return False

def hash_key(raw_key: str) -> str:
    """哈希处理密钥（用于董事密钥）"""
    return bcrypt.hashpw(
        raw_key.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

def verify_key(hashed_key: str, input_key: str) -> bool:
    """验证密钥"""
    try:
        return bcrypt.checkpw(
            input_key.encode('utf-8'),
            hashed_key.encode('utf-8')
        )
    except (ValueError, TypeError):
        return False

def generate_password_reset_token() -> str:
    """生成密码重置令牌（安全随机值）"""
    return secrets.token_urlsafe(32)