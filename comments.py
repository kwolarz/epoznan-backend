import requests
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass

@dataclass
class Comment:
    id: str
    text: str
    imageUrl: str
    author: str
    date: str
    likes: str
    dislikes: str
    numberOfResponses: str
    responses: list
    buried: bool
    banned: bool

def getComments(data, id, page):
    data.clear()
    data['comments'] = []
    url = 'https://epoznan.pl/showComments?news_id=' + id + '&page=' + page
    jsonData = requests.get(url)
    page = json.loads(jsonData.text)

    soup = BeautifulSoup(page['view'], 'html.parser')
    commentHTMLList = soup.find_all(class_='comments__item')
    data['numberOfComments'] = len(commentHTMLList)

    comments = []

    for i, comment in enumerate(commentHTMLList):
        isBuried = False
        isBanned = False

        commentText = comment.find(class_='comments__text').text.replace('\r\n', ' ').replace('  ', '').replace('\n', '').replace('\"', '"')
        if 'Ten komentarz zakopali czytelnicy, jeśli koniecznie chcesz go przeczytać kliknij' in commentText:
            commentText = commentText.replace('Ten komentarz zakopali czytelnicy, jeśli koniecznie chcesz go przeczytać kliknij', '')
            isBuried = True
        
        if 'Komentarz usunięty za złamanie regulaminu. IP autora zabezpieczono na potrzeby potencjalnego postępowania policji lub prokuratury.' in commentText:
            isBanned = True

        try:
            numberOfAnswers = comment.find(class_='comments__responses').text
            numberOfResponses = ''.join(x for x in numberOfAnswers if x.isdigit())
        except:
            numberOfResponses = '0'

        commentAuthor = comment.find(class_='comments__author').text
        commentDate = comment.find(class_='comments__date').text
        commentAvatarUrl = comment.find(class_='comments__avatar')['style'].split("('", 1)[1].split("')")[0]

        try:
            commentID = comment.find(class_='comments__delete')['onclick'].split("(", 1)[1].split(")")[0]
        except:
            commentID = 'none'

        try:
            commentLikes = comment.find(class_='comments__like comments__like--up').text
        except:
            commentLikes = '0'
        
        try:
            commentDislike = comment.find(class_='comments__like comments__like--down').text
        except:
            commentDislike = '0'

        listOfResponses = []
        for resp in range(i + 1, i + int(numberOfResponses) + 1):
            listOfResponses.append(resp)

        com = Comment(
            commentID,
            commentText,
            commentAvatarUrl,
            commentAuthor,
            commentDate,
            commentLikes,
            commentDislike,
            numberOfResponses,
            listOfResponses,
            isBuried,
            isBanned
        )

        comments.append(com)
        

    iter_com = iter(comments)
    for index, com in enumerate(iter_com):
        
        responses = []
        for resp in com.responses:
            responses.append({
                'id': comments[resp].id,
                'index': index,
                'text': comments[resp].text,
                'imageUrl': comments[resp].imageUrl,
                'author': comments[resp].author,
                'date': comments[resp].date,
                'likes': comments[resp].likes,
                'dislikes': comments[resp].dislikes,
                'numberOfResponses': comments[resp].numberOfResponses,
                'buried': comments[resp].buried,
                'banned': comments[resp].banned,
            })

        for _ in range(int(com.numberOfResponses)):
            next(iter_com)

        data['comments'].append({
            'id': com.id,
            'index': index,
            'text': com.text,
            'imageUrl': com.imageUrl,
            'author': com.author,
            'date': com.date,
            'likes': com.likes,
            'dislikes': com.dislikes,
            'numberOfResponses': com.numberOfResponses,
            'responses': responses,
            'buried': com.buried,
            'banned': com.banned,
        })


# getComments({}, '110299', '0')