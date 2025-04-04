import uvicorn
import secrets
from fastapi import FastAPI, Response, HTTPException, Cookie, Header, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from uuid import uuid4
from typing import Annotated



from src.models.models import FeedbackORM
from src.schemas.user_schemas import FeedbackDTO, FeedbackRequestDTO, CreateUserDTO, LoginDTO, Token, User, Role
from src.database import engine, my_session, Base

app = FastAPI()


"""
HELP
1.Header — используется для извлечения данных из заголовков HTTP-запроса. Например, с его помощью можно получить данные из 
    заголовков, таких как X-Token, User-Agent, и других метаданных запроса.

2.Path — используется для получения данных из части URL, которая является параметром пути (или маршрута). 
    Например, в URL /items/{item_id}, параметр item_id может быть извлечён с помощью Path.

3.Query — используется для извлечения данных из строки запроса (query parameters) после знака ? в URL. 
    Например, в URL /items/?name=apple&count=10, name и count будут параметрами запроса, которые можно получить с помощью Query.

4.Cookie — используется для получения данных из cookies, которые обычно передаются в заголовке Cookie в HTTP-запросе.
"""

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}

Base.metadata.create_all(engine)


def get_db():
    db = my_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return FileResponse("src/templates/index.html")
    # return FileResponse("./index.html",
    #                     filename="mainpage.html",
    #                     media_type="application/octet-stream") # Этот вариант для отправки файла к загрузке


@app.get("/users")
async def get_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


# Конечная точка для получения информации о пользователе по ID
@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.post("/feedback")
async def accept_feedback(feedback: FeedbackDTO, db: Session = Depends(get_db)) -> dict:
    db_feedback = FeedbackORM(name=feedback.name, message=feedback.message)
    db.add(db_feedback)
    db.commit()
    return {"message": f"Feedback received. Thank you, {feedback.name}"}

@app.get("/feedbacks")
async def get_feedbacks(db: Session = Depends(get_db)) -> list[FeedbackRequestDTO]:
    data = db.query(FeedbackORM).all()

    print(data)
    result = [FeedbackRequestDTO.model_validate(f) for f in data]
    return result







token_users = {}

user_login_db = {
    "user123":{
        "username": "user123",
        "password": "12345",
    }
}
@app.post("/login")
async def login(user_login: LoginDTO, response: Response) -> dict:
    """
    Эта функция принимает username и password, проверяет есть ли в базе, если есть то создает токен и сохраняет в cookie

    :param user_login: username and password
    :param response: Response
    :return: dict {session_token: token}
    """
    if user_login.username in user_login_db and user_login_db[user_login.username]["password"] == user_login.password:
        token = str(uuid4())
        token_users[user_login.username] = token

        response.set_cookie(key="session_token", value=token, httponly=True)
        return {"session_token": token}

    return {"message": "User not found"}


@app.get("/user")
async def user(session_token: str | None = Cookie(None)) -> dict:
    """
    End-point проверяет есть ли user по такому токену, принимает cookie. Eсли есть, то возвращает login and password
    :param session_token:
    :return: {login_user:login, password:password}
    """
    if session_token is not None:
        for k, v in token_users.items():
            if v == session_token:
                result_data = user_login_db[k]
                return {"username": result_data["username"], "password": result_data["password"]}

    raise HTTPException(status_code=404, detail="Unauthorized")


@app.get("/headers")
async def header_work(user_agent: Annotated[str | None, Header()] = None,
                      accept_language: Annotated[str | None, Header() ]= None
                      ) -> dict:

    if user_agent is None or accept_language is None:
        raise HTTPException(status_code=400, detail="Invalid or missing 'User-Agent' or Accept-Language header")
    if accept_language != "en-US,en;q=0.9,es;q=0.8":
        raise HTTPException(status_code=400, detail="Invalid Accept-Language. Format not supported header")
    return {"User-Agent": user_agent, "Accept-Language": accept_language}



#Реализация базовой аутентификации

security = HTTPBasic()

user_account_db = [
    LoginDTO(**{"username": "xasan_xasan", "password": "qwery123"}),
    LoginDTO(**{"username": "xasan_123", "password": "xasan123"})
]



async def get_user_auth(username: str):
    for my_user in user_account_db:
        if my_user.username == username:
            return my_user
    return None


async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    my_user = await get_user_auth(credentials.username)

    if my_user is None or not secrets.compare_digest(my_user.password, credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Basic"}
                            )
    return my_user

@app.get('/auth')
async def base_authenticate(user: LoginDTO = Depends(authenticate_user)):
    return {"message": "You got my secret, welcome"}





#Реализация JWT Аутентификации
from fastapi.security import OAuth2PasswordRequestForm
from src.security import  create_jwt_token, jwt_authenticate_user
from src.dependencies import get_current_user
from src.database import USERS_DATA_JWT, create_user
from src.hash_pass import get_password_hash


@app.post("/create_user")
async def add_user(new_user: CreateUserDTO)-> dict:

    user_id = len(USERS_DATA_JWT) + 1
    new_user.password = await get_password_hash(new_user.password)
    user_in_db = User(
        user_id=user_id,
        username=new_user.username,
        full_name=new_user.full_name,
        email=new_user.email,
        age=new_user.age,
        password=new_user.password,
        active=True,
        roles=[Role.GUEST]
    )
    result = await create_user(user_in_db)
    return result


@app.post("/singin")
async def get_token(user_in: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await jwt_authenticate_user(user_in.username, user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid login or password')
    token = create_jwt_token({"sub": user.username, "user_id": user.user_id})
    return Token(access_token=token, token_type="Bearer")



@app.get("/protected_resource", response_model=User)
async def protected_resource(current_user: User = Depends(get_current_user)):
    return current_user



#RBAC( Role Based Access Control)




if __name__ == "__main__":
    uvicorn.run(app)
