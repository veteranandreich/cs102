import requests
from bs4 import BeautifulSoup


def extract_news(soup):
    """ Extract news from a given web page """
    news_list = []
    t = soup.findAll("a", {"class": "storylink"})
    sub = soup.findAll("td", {"class": "subtext"})
    titles = [title.text for title in t]
    urls = [title['href'] for title in t]
    authors = soup.findAll('a', {"class": "hnuser"})
    authors_list = [author.text for author in authors]
    points = soup.findAll('span', {"class": "score"})
    points_list = []
    for point in points:
        begining = point.text.find(' ')
        points_list.append(point.text[:begining])
    comments = []
    for st in sub:
        iscom = st.text.find('comments')
        if iscom != -1:
            begining = st.text.rfind('|')
            comments.append(st.text[begining + 2:iscom - 1])
        else:
            comments.append('0')
    for i in range(30):  # 30 is an amount of news on 1 page
        news_list.append(
            {'author': authors_list[i],
             'comments': comments[i],
             'points': points_list[i],
             'title': titles[i],
             'url': urls[i]
             }
        )
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
