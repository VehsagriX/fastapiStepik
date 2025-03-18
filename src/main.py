import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from src.models.models import FeedbackORM
from src.schemas.user_schemas import FeedbackDTO, FeedbackRequestDTO, UserCreate
from src.database import engine, my_session, Base

app = FastAPI()

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




@app.post("/create_user")
async def create_user(user: UserCreate) -> UserCreate:
    return user




# @app.get("/custom")
# async def read_custom_message():
#     return {"message": "This is a custom message!"}
#
#
# @app.get("/users", response_model=User)
# async def read_users():
#     user_1 = User(name="John Doe", age=1)
#     return user_1
#
# # @app.post("/calculate")
# # def calculate(num1: int, num2: int):
# #     return {"result": num1 + num2}
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# @app.post("/user")
# async def get_user(user: User) -> User:
#
#     return user
#


if __name__ == "__main__":
    uvicorn.run(app)
