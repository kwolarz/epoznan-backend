import requests
from bs4 import BeautifulSoup

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

url = 'https://epoznan.pl/newsList-0-najswiezsze_wiadomosci'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
articles = []

articleHTMLList = soup.find_all(class_='masonryPosts__itemInner')
print(articleHTMLList[0])
for article in articleHTMLList:
    articleTitle = article.find('h4').text
    articleImgUrl = article.find(class_='masonryPosts__itemBg')['style'].split("('", 1)[1].split("')")[0]
    articleID = article['href']

    print(str(articleID))
