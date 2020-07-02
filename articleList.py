import requests
from bs4 import BeautifulSoup
import json

def getArticleList(data, tag, page):
    data.clear()
    data['articles'] = []
    url = 'https://epoznan.pl//showMoreNewsListDesktop-' + tag + '-' + page
    jsonData = requests.get(url)
    page = json.loads(jsonData.text)

    if page['success'] == 1:
        soup = BeautifulSoup(page['output'], 'html.parser')
        articleHTMLList = soup.find_all(class_='masonryPosts__itemInner')
        data['numberOfArticles'] = len(articleHTMLList)
        
        for article in articleHTMLList:
            isArticleHasUpdate = False

            articleTitle = article.find('h4').text.strip()
            if 'AKTUALIZACJA' in articleTitle:
                isArticleHasUpdate = True
                articleTitle = articleTitle.replace('\n                                        AKTUALIZACJA', '')

            
            try:
                articleImgUrl = article.find(class_='masonryPosts__itemBg')['style'].split("('", 1)[1].split("')")[0]
            except:
                articleImgUrl = 'https://www.poznan.pl/mim/turystyka/pictures/epoznan,pic1,1017,75153,134326,show2.jpg'
            articleID = article['href']

            data['articles'].append({
                'title': articleTitle,
                'imgUrl': articleImgUrl,
                'url': articleID,
                'update': isArticleHasUpdate
            })
            


# getArticleList({}, '0', '-1')