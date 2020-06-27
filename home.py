import requests
from bs4 import BeautifulSoup

def getHomeData(data):
    data.clear()
    data['middlePosts'] = []
    data['leftPosts'] = []
    data['todayEvents'] = []
    data['tomorrowEvents'] = []
    data['weekendEvents'] = []
    data['inCinema'] = []
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

        imgUrl = event.find(class_='eventsList__itemImage')['style'].split("('", 1)[1].split("')")[0]
        category = event.find(class_='eventsList__itemCategory').text
        info = event.find(class_='eventsList__itemInfo').text


        dataCategory = event['data-category']
        dataCategoryName = ''
        if dataCategory == '0':
            dataCategoryName = 'todayEvents'
        elif dataCategory == '1':
            dataCategoryName = 'tomorrowEvents'
        elif dataCategory == '2':
            dataCategoryName = 'weekendEvents'

        data[dataCategoryName].append({
            'title': title,
            'dataCategory': dataCategory,
            'category': category,
            'info': info,

        })

    
    inCinema = soup.find_all(class_='cinemaList__item')
    for movie in inCinema:
        imgUrl = movie.find(class_='cinemaList__itemImage')['style'].split("('", 1)[1].split("')")[0]

        data['inCinema'].append({
            'imgUrl': imgUrl,
        })

    weather = soup.find(class_='weatherList__boxAlertInner').text
    data['weather'] = weather




# getHomeData({})