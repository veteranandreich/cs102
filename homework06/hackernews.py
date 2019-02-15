from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    redirect("/classify")


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    id = request.query.id
    news = s.query(News).filter(News.id == id).one()
    news.label = label
    s.commit()
    redirect("/classify")


@route("/update")
def update_news():
    s = session()
    current_news = get_news('https://news.ycombinator.com/', 3)
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
    redirect("/classify")


@route("/classify")
def classify_news():
    s = session()
    classifier = NaiveBayesClassifier()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in labeled_news]
    y_train = [row.label for row in labeled_news]
    classifier.fit(x_train, y_train)
    blank_rows = s.query(News).filter(News.label == None).all()
    x = [row.title for row in blank_rows]
    labels = classifier.predict(x)
    good = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == 'good']
    maybe = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == 'maybe']
    never = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == 'never']
    return template('news', {'good': good, 'never': never, 'maybe': maybe})

if __name__ == "__main__":
    run(host="localhost", port=8080)
