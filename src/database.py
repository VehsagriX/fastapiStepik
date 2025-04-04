import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.schemas.user_schemas import User, Role
from src.hash_pass import get_password_hash


DATABASE_URL_FEEDBACK = f"sqlite:///feedback.db"
engine = create_engine(DATABASE_URL_FEEDBACK, echo=True)

my_session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass





USERS_DATA_JWT = {
    "aran": {
        "user_id": 1,
        "username": "aran",
        "password": "$2b$12$tq03gUXQneWVvO/zb3joqOqFAy5e8lkUpXbnUmYDeBXhuXpVXDtXi",  # qwerty123
        "age": 20,
        "email": "blabla@gmail.com",
        "full_name": "xasan irgashev",
        "active": True,
        "roles": [Role.USER],
    },
    "xasan": {
        "user_id": 2,
        "username": "xasan",
        "password": "$2b$12$BgADnTMnOLECsDOzpU8S7uHhF40kF5yXLb2sbJd8Euf/knNctiJHu", # qwerty111
        "age": 27,
        "email": "xasan@gmail.com",
        "full_name": "xasan irgashev",
        "active": False,
        "roles": [Role.ADMIN, Role.USER],
    },
    # в реальной БД храним только ХЭШИ паролей (например, с помощью библиотеки 'passlib') + соль (известная только нам добавка к паролю)
}


async def get_user(username: str):
    if username in USERS_DATA_JWT:
        return USERS_DATA_JWT[username]
    return None




async def create_user(new_user: User):
    USERS_DATA_JWT[new_user.username] = new_user
    print(USERS_DATA_JWT)
    return {"message": "success", "user": new_user}