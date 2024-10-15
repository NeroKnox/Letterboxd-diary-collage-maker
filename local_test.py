import requests 
from bs4 import BeautifulSoup 

username = 'neroknox'
year = '2023'
month = '07'

headers = {'User-Agent': 'Mozilla/5.0'}

diary = requests.get('https://letterboxd.com/'+username+'/films/diary/for/'+year+'/'+month+'/',headers=headers)
diary_soup = BeautifulSoup(diary.content, "html.parser")

films = diary_soup.find_all("td", class_="td-film-details")
print(films[0])
for film in films:
    div = film.find("div", class_="film-poster")
    print(div)
    film_name = div["data-film-name"]
    film_link = div["data-film-link"]
    print(film_name)
    print(film_link)