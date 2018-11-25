from collections import Counter
import datetime
import plotly
from api_models import Message
from typing import List, Tuple
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    c = Counter()
    for message in messages:
        date = fromtimestamp(message.date)
        c[date] += 1
    d, f = [], []
    for tup in c.most_common():
        d.append(tup[0])
        f.append(tup[1])
    a = (d, f)
    return a

def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly
    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    data = [plotly.graph_objs.Scatter(x=dates, y=freq)]
    plotly.plotly.plot(data)
