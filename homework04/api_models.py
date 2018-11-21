from typing import List, Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    """ Модель пользователя с базовыми полями """
    id: Optional[int]
    uid: Optional[int]
    first_name: str
    last_name: str
    online: int
    deactivated: Optional[str]


class User(BaseUser):
    """ Модель пользователя с необязательным полем дата рождения """
    bdate: Optional[str]


class Message(BaseModel):
    """ Модель сообщения """
    date: int
    from_id: int
    id: int
    text: Optional[str]
