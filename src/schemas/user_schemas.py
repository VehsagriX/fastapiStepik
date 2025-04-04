from enum import Enum

from pydantic import BaseModel, computed_field, EmailStr, PositiveInt


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt | None = None
    is_subscribed: bool = False


class UserDTO(BaseModel):
    name: str
    age: int

    @computed_field
    @property
    def is_adult(self) -> bool:
        """
           @computed_field:
           В некоторых фреймворках (например, в FastAPI или Pydantic) для того, чтобы вычисляемое поле показывалось в JSON-ответах,
           необходимо явно указать, что это поле должно быть вычисляемым.
           @computed_field — это аннотация, которая указывает фреймворку, что метод должен быть обработан как вычисляемое поле
           и включен в ответ JSON, даже если оно не является обычным атрибутом модели.
           """
        return self.age >= 18


class FeedbackDTO(BaseModel):
    name: str
    message: str


class FeedbackRequestDTO(FeedbackDTO):
    id: int

    class Config:
        from_attributes = True


class LoginDTO(BaseModel):
    username: str
    password: str



class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"



class CreateUserDTO(LoginDTO):

    full_name: str
    email: EmailStr
    age: int



class User(CreateUserDTO):
    user_id: int | None = None
    active: bool | None = None
    roles: list[Role] | None




class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
