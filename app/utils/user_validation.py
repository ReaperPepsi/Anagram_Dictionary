from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

def password_hasher(user_password: str) -> str:
    if not user_password:
        raise ValueError("Emtpy password provided")
    
    password_hash = PasswordHash((Argon2Hasher(),))
    return password_hash.hash(user_password)


def validate_login(user_password: str, db_password: str) -> bool:
    password_hash = PasswordHash((Argon2Hasher(),))
    return password_hash.verify(user_password, db_password)