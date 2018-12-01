from api import messages_get_history
from api_models import Message
from network import get_network
from network import plot_graph
from api import get_friends
from messages import count_dates_from_messages, plotly_messages_freq


'''messages = messages_get_history(175239807, offset=10, count=50)
messages_list = [Message(**mes) for mes in messages]
dates_freqs = count_dates_from_messages(messages_list)
plotly_messages_freq(dates_freqs[0], dates_freqs[1])'''

friends = get_friends(141948816, fields='bdate')
ids = []
names = []
for friend in friends:
    ids.append(friend['uid'])
    names.append(friend['first_name'] + ' ' + friend['last_name'])
edges = get_network(ids)
plot_graph(edges, names)

