from goose3 import Goose
import requests
from bs4 import BeautifulSoup


def getArticle(data, url):
    data.clear()
    g = Goose()
    url = 'https://epoznan.pl/' + url
    page = requests.get(url)
    article = g.extract(raw_html=page.text)
    soup = BeautifulSoup(page.text, 'html.parser')

    #get title
    title = article.title
    data['title'] = title

    #get date
    dateDiv = soup.find(class_='post__date')
    date = dateDiv.find('span').text
    data['publishDate'] = date

    #get top image
    try:
        topImage = article.opengraph['image']
    except:
        topImage = 'https://www.poznan.pl/mim/turystyka/pictures/epoznan,pic1,1017,75153,134326,show2.jpg'

    data['topImageURL'] = topImage

    #get text
    text = article.cleaned_text.replace('\n\n', '\n')
    # numberOfNewlines = 0
    # if '\n\n' in text[:10]:
    #     numberOfNewlines += 1
    
    # toReplace = '' + '\n'
    # for _ in range(numberOfNewlines):
    #     toReplace += '\n'
    
    # text = text[0:10]
    
    #get description
    try:
        description = article.opengraph['description']
        if description in text:
            text = text.replace(description, '')
    except:
        description = ''


    data['text'] = text
    data['description'] = description

    #get author
    author = soup.find(class_='post__author').text
    author = author.replace('\n', '').replace('  ', '')
    data['author'] = author

    #get youtube data
    youtubeURL = []
    numberOfYT = 0
    for movie in article.infos['movies']:
        if movie['provider'] == 'youtube':
            numberOfYT += 1
            youtubeURL.append(movie['src'])

    data['numberOfYT'] = numberOfYT
    data['youtubeURL'] = youtubeURL

    #get comments
    #cancelled in this place due to many data in one scope

    #get number of commetns
    try:
        numberOFCommentsDiv = soup.find(class_='postSidebar__actionBox postSidebar__actionBox--lightBlue')
        numberOfComments = numberOFCommentsDiv.find_all('span')[1].text.split('(',1)[1].split(')')[0]
    except:
        numberOfComments = '0'
    
    data['numberOfComments'] = numberOfComments

    #get tags
    data['tags'] = []
    try:
        listOfTags = soup.find_all(class_='featuredVideo__tag')
        for tag in listOfTags:
            tagName = tag.text
            tagID = tag['href'].split('newsList-', 1)[1].split('-')[0]
            data['tags'].append({
                'tagName': tagName,
                'tagID': tagID
            })
    except:
        data['tags'] = []

    #get list of images
    data['imagesURL'] = []
    for imgUrl in article.infos['links']:
        if 'epoznan' in imgUrl:
            data['imagesURL'].append({
                'imgUrl': imgUrl,
            })

    #get update data
    data['updates'] = []
    articleHasUpdate = False
    try:
        listOfUpdates = soup.find_all(class_='update__item')
        if listOfUpdates:
            articleHasUpdate = True
    except:
        articleHasUpdate = False

    data['articleHasUpdate'] = articleHasUpdate
    if articleHasUpdate:
        for update in listOfUpdates:
            updateDivText = update.div.text.replace('\n', '').replace('  ', '')
            updateText = update.text.replace('\n', '').replace('  ', '').replace(updateDivText+updateDivText, '')
            updateDate = update.find(class_='update__hour-2').text.replace('Aktualizacja', '')
            data['updates'].append({
                'updateText': updateText,
                'updateDate': updateDate,
            })
    

    hasFacebookVideo = False
    try:
        facebookVideo = soup.find(class_='post__content').find('iframe')['src']
        hasFacebookVideo = True
    except:
        facebookVideo = ''
        hasFacebookVideo = False
    
    if not 'facebook' in facebookVideo:
        facebookVideo = ''
        hasFacebookVideo = False


    data['facebookVideos'] = {
        'hasFacebookVideo': hasFacebookVideo,
        'embededURL': facebookVideo,
    }

    data['tweets'] = []
    for tweet in article.infos['tweets']:
        data['tweets'].append({
            'source': str(tweet),
        })

    #print(data)
#getArticle({}, 'news-news-104091-need_for_speed_ulicami_poznania_za_kierownica_corsy_siedzial_14_latek_wideo')
#getArticle({}, 'news-news-87737-sondaz_preferencjji_wyborczych_w_regionach_poznan_w_dalszym_ciagu_bastionem_po')
#getArticle({}, 'news-news-107686-posel_pis_przyjechal_do_jednej_z_podpoznanskich_gmin_z_czekiem_wojt_zaskoczyl_go_rachunkiem')