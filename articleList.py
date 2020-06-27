import requests
from bs4 import BeautifulSoup
import json

class Article:
    title = ''  
    imgUrl = ''
    id = 0
    date = ''

    def __init__(self, title, imgUrl, id, date):
        self.title = title
        self.imgUrl = imgUrl
        self.id = id
        self.date = date


def getArticleList(data, tag, page):
    data.clear()
    data['articles'] = []
    url = 'https://epoznan.pl//showMoreNewsListDesktop-' + tag + '-' + page
    jsonData = requests.get(url)
    page = json.loads(jsonData.text)

    if page['success'] == 1:
        soup = BeautifulSoup(page['output'], 'html.parser')
        articleHTMLList = soup.find_all(class_='masonryPosts__itemInner')
        print(articleHTMLList[0])
        data['numberOfArticles'] = len(articleHTMLList)
        for article in articleHTMLList:
            isArticleHasUpdate = False
            articleTitle = article.find('h4').text.strip()
            if 'AKTUALIZACJA' in articleTitle:
                isArticleHasUpdate = True
                articleTitle = articleTitle.replace('\n                                        AKTUALIZACJA', '')
            articleImgUrl = article.find(class_='masonryPosts__itemBg')['style'].split("('", 1)[1].split("')")[0]
            articleID = article['href']
            data['articles'].append({
                'title': articleTitle,
                'imgUrl': articleImgUrl,
                'url': articleID,
                'update': isArticleHasUpdate
            })
            


# getArticleList({}, '0', '-1')