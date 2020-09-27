from flask import Flask
from flask import jsonify
import json
from articleList import getArticleList
from article import getArticle
from home import getHomeData
from comments import getComments
from movie import getMovie


data = {}
app = Flask(__name__)

@app.route('/')
def main():
    return 'epoznan.pl'

@app.route('/news/<tag>/<page>')
def news(tag, page):
    getArticleList(data, tag, page)
    return json.dumps(data)


@app.route('/article/<url>')
def article(url):
    getArticle(data, url)
    return jsonify(data)


@app.route('/home')
def home():
    getHomeData(data)
    return json.dumps(data)


@app.route('/comments/<id>/<page>')
def comments(id, page):
    getComments(data, id, page)
    return json.dumps(data)

@app.route('/movie/<url>')
def movie(url):
    getMovie(data, url)
    return json.dumps(data)

if __name__ == '__main__':
    # app.run(host='0.0.0.0') 
    app.run()