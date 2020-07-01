from flask import Flask
import json
from articleList import getArticleList
from article import getArticle
from home import getHomeData


data = {}
app = Flask(__name__)

@app.route('/news/<tag>/<page>')
def news(tag, page):
    getArticleList(data, tag, page)
    return json.dumps(data)


@app.route('/article/<url>')
def article(url):
    getArticle(data, url)
    return json.dumps(data)


@app.route('/home')
def home():
    getHomeData(data)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0') 