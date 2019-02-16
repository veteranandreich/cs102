from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from sqlalchemy.orm import load_only


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    news_id = request.query.id
    news = s.query(News).filter(News.id == news_id).one()
    news.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    current_news = get_news('https://news.ycombinator.com/', 1)
    existing_news = s.query(News).options(load_only("title", "author")).all()
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
    s = session()
    classifier = NaiveBayesClassifier()
    train_news = s.query(News).filter(News.label != None).options(load_only("title", "label")).all()
    x_train = [row.title for row in train_news]
    y_train = [row.label for row in train_news]
    classifier.fit(x_train, y_train)
    test_news = s.query(News).filter(News.label == None).all()
    x = [row.title for row in test_news]
    labels = classifier.predict(x)
    good = [test_news[i] for i in range(len(test_news)) if labels[i] == 'good']
    maybe = [test_news[i] for i in range(len(test_news)) if labels[i] == 'maybe']
    never = [test_news[i] for i in range(len(test_news)) if labels[i] == 'never']
    return template('news', {'good': good, 'never': never, 'maybe': maybe})


if __name__ == "__main__":
    run(host="localhost", port=8080)
