#PassLib - это отличный пакет Python для работы с хэшами паролей.

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

my_password = "random123"

def verify_password(plain_password, hashed_password)-> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password)-> str:
    return pwd_context.hash(password)



