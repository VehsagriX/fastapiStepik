#PassLib - это отличный пакет Python для работы с хэшами паролей.

from passlib.context import CryptContext


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# async def verify_password(plain_password, hashed_password)-> bool :
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# async def get_password_hash(password)-> str:
#     return pwd_context.hash(password)

import bcrypt


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


async def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
