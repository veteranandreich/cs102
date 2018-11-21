import requests
import time
from config import VK_CONFIG as vk
from typing import Optional


def get(url: str, params={}, timeout=5, max_retries=10, backoff_factor=0.3) -> Optional[requests.models.Response]:
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for n in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=(timeout, 3))
            return response
        except requests.exceptions.RequestException:
            if n == max_retries - 1:
                raise
            delay = backoff_factor * 2 ** n
            time.sleep(delay)


def get_friends(user_id: int, fields="") -> list:
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'access_token': vk['access_token'],
        'user_id': user_id,
        'fields': fields,
        'version': vk['version']
    }

    query = "{domain}/friends.get?".format(domain=vk['domain'])
    response = get(query, query_params)
    try:
        return response.json()['response']['items']
    except TypeError:
        return response.json()['response']


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


def get_network(users_ids: list, as_edgelist=True) -> list:
    user_num = 0
    edge_list = []
    matrix = [[0] * len(users_ids) for _ in range(len(users_ids))]
    for user in users_ids:
        if user_num % 2 == 0:
            time.sleep(1)
        try:
            friend_list = get_friends(user)
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
