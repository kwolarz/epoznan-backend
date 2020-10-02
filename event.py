import requests
from bs4 import BeautifulSoup

def getEvent(data, url):
    data.clear()
    url = 'https://epoznan.pl/' + url
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    title = soup.find(class_='post__title').text.replace('\n', '').replace('  ', '')
    imageUrl = soup.find(class_='post__featuredImage')['src']
    desc = soup.find('h2').text

    postDiv = soup.find(class_='post__content')
    for br in postDiv.find_all('br'):
        br.replace_with('\n')
    text = postDiv.find('p').text.replace('\n\n', '\n')

    print(title)
    print(imageUrl)
    print(desc)
    print(text)

    data['title'] = title
    data['imageUrl'] = imageUrl
    data['description'] = desc
    data['text'] = text


getEvent({}, 'culture-event-2457-gary_moore_tribute_band_feat_jack_moore')