import datetime as dt
from statistics import median
from typing import Optional
from datetime import datetime, date
from api import get_friends
from api_models import User


def age_predict(user_id: int) -> float:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')
    age_list = []
    for friend in friends:
        person = User(**friend)
        try:
            bday = person.bdate
            s = bday.count('.')
        except AttributeError:
            pass
        else:
            if s == 2:
                d1 = datetime.strptime(bday, "%d.%m.%Y")
                d2 = datetime.date(datetime.now())
                age = d2.year - d1.year - ((d2.month, d2.day) < (d1.month, d1.day))
                age_list.append(age)
    if age_list:
        return float(median(age_list))
