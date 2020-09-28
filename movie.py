import requests
from bs4 import BeautifulSoup

def getMovie(data, url):
    data.clear()
    url = 'https://epoznan.pl/' + url
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    title = soup.find(class_='post__title').text.replace('\n', '').replace('  ', '')
    imageUrl = soup.find(class_='gallery__imageContainer')['href']

    contentDiv = soup.find(class_='post__content')
    text = contentDiv.find_all('p')[0].text.replace('\n', '').replace('  ', '')
    cast = contentDiv.find_all('p')[1].text.replace('\n', '').replace('  ', '')

    dates = []
    post = soup.find(class_='singlePost__main')
    datesHTML = post.find_all('p')[2:]
    for index, date in enumerate(datesHTML):
        # print(date.text.replace('\n', '').replace('  ', ''))
        date = date.text.replace('\n', '').replace('  ', '')
        dates.append({
            str(index + 1): date,
        })
        # dates.append(date)

    repertoire = {}
    for i, header in enumerate(post.find_all('p')[2:], 1):
        next_tag = header
        j = 1

        places = []
        hourss = []

        while True:
            next_tag = next_tag.next_sibling
            if next_tag is None or next_tag.name == 'p' or next_tag.name == 'div':
                break
            if next_tag.name is not None:
                # print('{} - {}/{} - {}'.format(i, header.text, j, next_tag.string))
                # print(next_tag.text)

                place = next_tag.find(class_='eventsList__itemInfo icon-location').text
                hours = next_tag.find(class_='eventsList__itemInfo icon-time').text.replace('.', ':').split(', ')
                # print(places)

                places.append(place)
                hourss.append(hours)
                repertoire[str(i)] = []


                j += 1
        
        for index in range(len(places)): 
            repertoire[str(i)].append({
                'place': places[index],
                'hours': hourss[index],
            })

    # print(places)
    # print(hourss)
    # print(title)
    # print(imageUrl)
    # print(text)
    # print(cast)
    # print(dates)

    data['title'] = title
    data['description'] = text
    data['cast'] = cast
    data['poster'] = imageUrl
    data['dates'] = dates
    data['repertoire'] = repertoire

getMovie({}, 'culture-film-29558-mulan')
#getMovie({}, 'culture-film-29547-25_lat_niewinnosci_sprawa_tomka_komendy')