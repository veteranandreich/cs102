import requests
from bs4 import BeautifulSoup


def extract_news(soup):
    """ Extract news from a given web page """
    news_list = [{'author': '',
                  'comments': 0,
                  'points': 0,
                  'title': '',
                  'url': ''} for i in range(30)]
    rows = soup.findAll("tr", {"class": "athing"})
    for idx, row in enumerate(rows):
        title = row.find('a', {"class": "storylink"}).text
        url = row.find('a', {"class": "storylink"})['href']
        news_list[idx]['title'] = title
        news_list[idx]['url'] = url
    sub_rows = soup.findAll("td", {"class": "subtext"})
    for idx, sub in enumerate(sub_rows):
        try:
            points = ''.join([d for d in sub.find('span', {"class": "score"}).text if d.isdigit()])
        except AttributeError:
            points = None
        author = sub.find('a', {"class": "hnuser"})
        if author:
            author = author.text
        else:
            author = None
        iscom = sub.text.find('comments')
        if iscom != -1:
            begining = sub.text.rfind('|')
            comments = sub.text[begining + 2:iscom - 1]
        else:
            comments = 0
        news_list[idx]['points'] = points
        news_list[idx]['author'] = author
        news_list[idx]['comments'] = comments
    return news_list


def extract_next_page(soup):
    """ Extract next page URL """
    a = soup.find('a', {"class": "morelink"})
    return a['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
