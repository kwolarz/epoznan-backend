import requests
from bs4 import BeautifulSoup

def getWeather(data):
    data.clear()
    url = 'https://epoznan.pl/weather'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    