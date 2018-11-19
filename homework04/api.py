import requests
import random
import time
from datetime import datetime
from config import VK_CONFIG as vk
from config import PLOTLY_CONFIG as pl
from api_models import Message
import plotly
from igraph import Graph, plot
import numpy

plotly.tools.set_credentials_file(username=pl['username'], api_key=pl['api_key'])


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    n = 0
    delay = 0.5
    while n < max_retries:
        try:
            response = requests.get(url.format(**params), timeout=(timeout, 3))
        except requests.exceptions.ReadTimeout:
            print('Oops. Read timeout occured')
        except requests.exceptions.ConnectTimeout:
            print('Oops. Connection timeout occured!')
        except requests.exceptions.ConnectionError:
            print('Seems like dns lookup failed..')
        except requests.exceptions.HTTPError as err:
            print('Oops. HTTP Error occured')
            print('Response is: {content}'.format(content=err.response.content))
        else:
            return response
        delay = min(delay * backoff_factor, 10)
        delay = delay + random.normalvariate(delay, 0.1)
        time.sleep(delay)


def get_friends(user_id, fields=""):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': vk['domain'],
        'access_token': vk['access_token'],
        'user_id': user_id,
        'fields': fields,
        'version': vk['version']
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=[version]"
    response = get(query, query_params)
    return response.json()


def messages_get_history(user_id, offset=0, count=200):
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    query_params = {
        'domain': vk['domain'],
        'access_token': vk['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'version': vk['version']
    }
    url = "{domain}/messages.getHistory?offset={offset}&count={count}&user_id={user_id}&" \
          "access_token={access_token}&v={version}".format(**query_params)
    response = requests.get(url)
    messages = response.json()['response']['items']
    return messages


def count_dates_from_messages(messages):
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    date_list = []
    frequency = []
    k = 0
    for m in messages:
        message = Message(**m)
        date = datetime.fromtimestamp(message.date).strftime("%Y-%m-%d")
        if date not in date_list:
            if k:
                frequency.append(k)
            date_list.append(date)
            k = 1
        else:
            k += 1
    frequency.append(k)
    freq_list = []
    freq_list.append(date_list)
    freq_list.append(frequency)
    return freq_list


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly
    :param freq_list: список дат и их частот
    """

    data = [plotly.graph_objs.Scatter(x=freq_list[0], y=freq_list[1])]
    plotly.plotly.plot(data)


def get_network(users_ids, as_edgelist=True):
    pass

def plot_graph(graph):
    pass
