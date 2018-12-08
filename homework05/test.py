import config
import requests
import datetime
from bs4 import BeautifulSoup

week_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
dt = datetime.datetime.now()
st ='{} {} {} 12:33'.format(dt.year, dt.day, dt.month)
datetime_object = datetime.datetime.strptime(st, '%Y %d %m %H:%M')
print(datetime_object
      )