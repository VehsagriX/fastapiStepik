from datetime import  timedelta, datetime, timezone

import jwt  # тут используем библиотеку PyJWT
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.hash_pass import verify_password
from src.database import get_user
from src.schemas.user_schemas import User

"""
JWT состоит из трех частей, разделённых точками: заголовка (header), полезной нагрузки (payload) и подписи (signature):

1. Заголовок (Header): Содержит метаданные о токене, такие как алгоритм подписи (например, HMAC SHA256 или RSA).

2. Полезная нагрузка (Payload): Содержит утверждения, которые могут включать информацию о пользователе, такие как имя 
    или роль, а также дополнительную информацию. Эти данные не зашифрованы, а только кодируются, поэтому не следует 
    хранить конфиденциальную информацию в этой части.

3.Подпись (Signature): Генерируется с использованием секретного ключа и алгоритма подписи. Это гарантирует, что токен не 
    был изменён, и что он был создан авторизованным сервером.
"""

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = os.getenv(
    "SECRET_KEY")  # в реальной практике используем что-нибудь вроде команды Bash (Linux) 'openssl rand -hex 32'

ALGORITHM = "HS256"  # плюс в реальной жизни устанавливаем "время жизни" токена
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=3)

# Пример информации из БД







# Функция для получения пользовательских данных на основе имени пользователя
async def jwt_authenticate_user(username: str, password: str):
    user = await get_user(username)
    print(user)
    user = User(**user)
    if not user:
        return False
    if not await verify_password(password, user.password):
        return False
    return user


# Функция для создания JWT токена
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY,
                      algorithm=ALGORITHM)  # кодируем токен, передавая в него наш словарь с нужной информацией


# Функция получения User'а по токену
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # декодируем токен
        return payload.get("sub")  # извлекаем утверждение о пользователе (subject); можем также использовать другие данные,
                                    # например, "iss" (issuer) или "exp" (expiration time)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Истекло время жизни токена')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Неправильный токен',
                             headers={"WWW-Authenticate": "Bearer"})  # логика обработки ошибки декодирования токена


