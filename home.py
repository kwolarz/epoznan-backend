import requests
from bs4 import BeautifulSoup

def getHomeData(data):
    data.clear()
    data['middlePosts'] = []
    data['leftPosts'] = []
    data['todayEvents'] = []
    data['tomorrowEvents'] = []
    data['weekendEvents'] = []
    url = 'https://epoznan.pl'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')


    middlePosts = soup.find_all(class_='masonryPosts__itemInner')
    for article in middlePosts:
        isArticleHasUpdate = False
            
        articleTitle = article.find('h4').text.strip()
        if 'AKTUALIZACJA' in articleTitle:
            isArticleHasUpdate = True
            articleTitle = articleTitle.replace('\n                                        AKTUALIZACJA', '')

        articleImgUrl = article.find(class_='masonryPosts__itemBg')['style'].split("('", 1)[1].split("')")[0]
        articleID = article['href']

        data['middlePosts'].append({
            'title': articleTitle,
            'imgUrl': articleImgUrl,
            'url': articleID,
            'update': isArticleHasUpdate
        })

    leftPosts = soup.find_all(class_='postItem')
    for post in leftPosts:
        title = post.find('h3').text
        publishDate = post.find('a', class_='postItem__category').text
        imgUrl = post.find(class_='postItem__imageInner')['style'].split("('", 1)[1].split("')")[0]
        url = post.find('a', class_='postItem__category')['href']

        data['leftPosts'].append({
            'title': title,
            'publishDate': publishDate,
            'imgUrl': imgUrl,
            'url': url
        })

    

    events = soup.find_all(class_='eventsList__item')
    for event in events:
        title = event.find('h4').text
        if '\n' in title:
            title = title.replace('\n                  ', '')
            title = title.replace('  ', '')

        category = event['data-category']
        categoryName = ''
        if category == '0':
            categoryName = 'todayEvents'
        elif category == '1':
            categoryName = 'tomorrowEvents'
        elif category == '2':
            categoryName = 'weekendEvents'

        data[categoryName].append({
            'title': title,
            'category': category
        })

    data['ilosc'] = len(events)




# getHomeData({})