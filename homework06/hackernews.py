from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    id = request.query.id
    news = s.query(News).filter(News.id == id).one()
    news.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    current_news = get_news('https://news.ycombinator.com/', 10)
    existing_news = s.query(News).all()
    existing_t_a = [(news.title, news.author) for news in existing_news]
    for news in current_news:
        if (news['title'], news['author']) not in existing_t_a:
            news_add = News(title=news['title'],
                            author=news['author'],
                            url=news['url'],
                            comments=news['comments'],
                            points=news['points'])
            s.add(news_add)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    psss

if __name__ == "__main__":
    run(host="localhost", port=8080)