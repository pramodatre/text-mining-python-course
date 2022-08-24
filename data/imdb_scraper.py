# https://www.dataquest.io/blog/web-scraping-beautifulsoup/
from requests import get
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
print(type(html_soup))

movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
print(type(movie_containers))
print(len(movie_containers))

first_movie = movie_containers[0]
first_name = first_movie.h3.a.text
print(first_name)

first_year = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
first_year = first_year.text
print(first_year)

first_rating = first_movie.strong
first_imdb = float(first_rating.text)
print(first_imdb)

first_meta = first_movie.find('span', class_ = 'metascore favorable')
print(first_meta.text)