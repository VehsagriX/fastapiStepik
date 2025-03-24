import uvicorn
from fastapi import BackgroundTasks, FastAPI, Cookie, Response
from datetime import datetime

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """
    Эта функция демонстрирует реализацию фоновых задач с помощью класса BackgroundTasks
    :param email:
    :param background_tasks:
    :return:
    """
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}







@app.get("/")
async def root(last_visit=Cookie(default=None)):
    """Если сразу запустить get /, то last_vizit: None
        Но если отправить пост запрос, а после
        снова запустить get будет last_visit: с датой отправки post запроса.
        Можем извлекать данные cookie и работать с ними в своих обработчиках маршрутов точно так же,
        как с любыми другими параметрами запроса. Это продемонстрировано в этой функции
    """

    return {"last_visit": last_visit}
@app.post('/')
async def set_cookie(response: Response):
    """Эта функция как пример, как отправляются куки в Fast api"""
    response.set_cookie(key="last_visit", value=f'{datetime.now()}')#тут устанавливаются файлы cookie в ответе,
    # используя метод set_cookie
    """
    Метод set_cookie позволяет настраивать следующие параметры:
    key: имя cookie.
    value: значение cookie.
    max_age: срок действия cookie (в секундах).
    expires: дата и время истечения срока действия cookie.
    path: путь, с которым cookie будет доступна.
    domain: домен, с которым cookie будет доступна.
    secure: если True, cookie будет передаваться только по защищенному соединению (https).
    httponly: если True, cookie не будет доступна через JavaScript, что повышает безопасность.
    samesite: позволяет ограничить, как cookie будет передаваться с запросами из других сайтов.
    """


if __name__ == "__main__":
    uvicorn.run(app)
