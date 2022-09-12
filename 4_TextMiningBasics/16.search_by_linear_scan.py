import time
import pandas as pd


# Read the movie review data
movie_dataset = pd.read_csv("data/imdb_movie_ratings/clean_movie_ratings_2000_2022.csv")
print(movie_dataset)
# Search for keywords in movie descriptions
unique_movies = movie_dataset.drop_duplicates(subset=["movie"])
while True:
    key_word = input("Enter search term:")
    if key_word == "":
        break
    st = time.time()
    num_documents_searched = 0
    for row in unique_movies.itertuples():
        if key_word in row.description:
            print(f"{row.movie}, {row.year}")
            print(f"{row.description}")
            print("------------\n")
        num_documents_searched += 1
    et = time.time()
    print(f"searched {num_documents_searched} documents in {et - st} seconds")
    search_time = et - st
    search_time_in_hours_900million = (search_time * 900 * 10**6) / (60 * 60)
    print(
        f"With this search engine, to search 900 million documents, it takes: {search_time_in_hours_900million} hours"
    )
    print("************************************")
