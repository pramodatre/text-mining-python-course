# https://www.dataquest.io/blog/web-scraping-beautifulsoup/
import os
import pandas as pd
from warnings import warn
from time import time
from time import sleep
from random import randint
from requests import get
from bs4 import BeautifulSoup

warn("Warning Simulation")


def single_movie_data_extractor(movie_container):
    meta = movie_container.find("div", "ratings-metascore")
    if meta is None:
        return None
    movie_name = movie_container.h3.a.text
    year = movie_container.h3.find("span", class_="lister-item-year text-muted unbold")
    year = year.text
    rating = movie_container.strong
    imdb_rating = float(rating.text)
    # metascore appears with favorable, unfavorable or mixed
    # So, we will just used metascore which is enough to capture
    # the metascore value for all the three cases
    meta = movie_container.find("span", class_="metascore")
    meta_rating = meta.text
    number_of_votes = movie_container.find("span", attrs={"name": "nv"})
    number_of_votes = number_of_votes["data-value"]
    # Get movie description
    ps = movie_container.find_all("p", class_="text-muted")
    description = ps[1].text
    return {
        "movie": movie_name,
        "year": year,
        "imdb": imdb_rating,
        "metascore": meta_rating,
        "votes": number_of_votes,
        "description": description,
    }


def collect_movie_ratings_from_imdb_site():
    pages = [str(i) for i in range(1, 5)]
    year_urls = [str(i) for i in range(2000, 2023)]
    movie_data_list = []
    requests = 0
    start_time = time()
    for year_url in year_urls:
        for page in pages:
            url = f"https://www.imdb.com/search/title?release_date={year_url}&sort=num_votes,desc&page={page}"
            response = get(url)
            # Randomly delay to ensure we don't overwhelm the server
            sleep(randint(8, 15))
            # Update request time and number of requests
            requests += 1
            elapsed_time = time() - start_time
            print(
                f"Request: {requests}; Frequency: {requests / elapsed_time} requests/second"
            )

            # Throw a warning for non-200 status codes
            if response.status_code != 200:
                warn(
                    "Request: {}; Status code: {}".format(
                        requests, response.status_code
                    )
                )

            html_soup = BeautifulSoup(response.text, "html.parser")
            movie_containers = html_soup.find_all(
                "div", class_="lister-item mode-advanced"
            )
            for movie_container in movie_containers:
                movie_data = single_movie_data_extractor(movie_container)
                if movie_data is not None:
                    movie_data_list.append(movie_data)

    movie_ratings_data = pd.DataFrame.from_dict(movie_data_list)
    print(movie_ratings_data)
    movie_ratings_data.to_csv("movie_ratings_2000_2022.csv", index=False)


def test_single_page_extraction():
    url = f"https://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1"
    response = get(url)
    html_soup = BeautifulSoup(response.text, "html.parser")
    # print(type(html_soup))
    movie_containers = html_soup.find_all("div", class_="lister-item mode-advanced")
    movie_data_list = []
    for movie_container in movie_containers:
        movie_data = single_movie_data_extractor(movie_container)
        if movie_data is not None:
            movie_data_list.append(movie_data)

    print(pd.DataFrame.from_dict(movie_data_list))


if __name__ == "__main__":
    # Test data extraction for a single page
    # test_single_page_extraction()

    # Run multiple page extraction
    collect_movie_ratings_from_imdb_site()
