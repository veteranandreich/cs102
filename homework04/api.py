import requests
import random
import time
from datetime import datetime
from config import VK_CONFIG as vk
from config import PLOTLY_CONFIG as pl
from api_models import Message, User
import plotly
import igraph
from igraph import Graph, plot
from typing import Optional

plotly.tools.set_credentials_file(username=pl['username'], api_key=pl['api_key'])


def get(url: str, params={}, timeout=5, max_retries=10, backoff_factor=0.3) -> Optional[requests.models.Response]:
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


def get_friends(user_id: int, fields="") -> Optional[dict]:
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
    if response:
        return response.json()
    return None


def messages_get_history(user_id: int, offset=0, count=200) -> list:
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


def count_dates_from_messages(messages: list) -> list:
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


def plotly_messages_freq(freq_list: list) -> None:
    """ Построение графика с помощью Plot.ly
    :param freq_list: список дат и их частот
    """
    data = [plotly.graph_objs.Scatter(x=freq_list[0], y=freq_list[1])]
    plotly.plotly.plot(data)


def get_network(users_ids: list, as_edgelist=True) -> list:
    user_num = 0
    edge_list = []
    matrix = [[0] * len(users_ids) for _ in range(len(users_ids))]
    for user in users_ids:
        if user_num % 2 == 0:
            time.sleep(1)
        try:
            friend_list = get_friends(user)['response']
        except KeyError:
            continue
        else:
            for friend in friend_list:
                if friend in users_ids:
                    edge_list.append((users_ids.index(user), users_ids.index(friend)))
                    matrix[users_ids.index(user)][users_ids.index(friend)] = 1
            user_num += 1
    if as_edgelist:
        return edge_list
    return matrix


def plot_graph(edge_list: list, name_list=[]) -> None:
    if name_list == 0:
        vertices = [i for i in range(len(edge_list))]
    else:
        vertices = name_list
    g = Graph(vertex_attrs={"label": vertices},
              edges=edge_list, directed=False)
    g.simplify(multiple=True, loops=True)
    N = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "bbox": (2000, 2000),
        "margin": 100,
        "vertex_label_dist": 1.6,
        "edge_color": "gray",
        "autocurve": True,
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }

    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)
