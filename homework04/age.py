from statistics import median
from typing import Optional
from datetime import datetime
from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = [User(**i) for i in get_friends(user_id, 'bdate')]
    current_date = datetime.date(datetime.now())
    age_list = []
    for person in friends:
        bday = person.bdate
        try:
            bd = datetime.strptime(bday, "%d.%m.%Y")
        except (ValueError, TypeError):
            pass
        else:
            age = current_date.year - bd.year - ((current_date.month, current_date.day) < (bd.month, bd.day))
            age_list.append(age)
    if age_list:
        return float(median(age_list))
