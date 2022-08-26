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


def collect_movie_ratings_from_imdb_site():
    pages = [str(i) for i in range(1, 5)]
    year_urls = [str(i) for i in range(2000, 2018)]
    ratings_data_list = []
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

            # Break the loop if the number of requests is greater than expected
            if requests > 72:
                warn("Number of requests was greater than expected.")
                break

            html_soup = BeautifulSoup(response.text, "html.parser")
            # print(type(html_soup))
            movie_containers = html_soup.find_all(
                "div", class_="lister-item mode-advanced"
            )
            # print(type(movie_containers))
            # print(len(movie_containers))
            for movie_container in movie_containers:
                # Some movies may not have metascore and we want to skip those
                meta = movie_container.find("div", "ratings-metascore")
                if meta is None:
                    continue
                movie_name = movie_container.h3.a.text
                year = movie_container.h3.find(
                    "span", class_="lister-item-year text-muted unbold"
                )
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
                ratings_data_list.append(
                    {
                        "movie": movie_name,
                        "year": year,
                        "imdb": imdb_rating,
                        "metascore": meta_rating,
                        "votes": number_of_votes,
                    }
                )

    movie_ratings_data = pd.DataFrame(ratings_data_list)
    print(movie_ratings_data)
    movie_ratings_data.to_csv("movie_ratings.csv", index=False)


if __name__ == "__main__":
    if os.path.exists("movie_ratings.csv"):
        movie_ratings_data = pd.read_csv("movie_ratings.csv")
        print(movie_ratings_data)
    else:
        collect_movie_ratings_from_imdb_site()
