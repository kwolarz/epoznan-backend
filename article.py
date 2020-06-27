from newspaper import Article


def getArticle(data, url):
    article = Article('https://epoznan.pl/' + url)
    article.download()
    article.parse()
    
    print(article.summary)

# getArticle({}, 'news-news-107304-rozpoczal_sie_remont_torowiska_na_pulaskiego')