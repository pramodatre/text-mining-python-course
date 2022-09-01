import pandas as pd

""" 
1. What does this data contain?
* Movie review data for 22 years (starting from
year 2000 to year 2022). 
* Movies are ordered by the number of votes and movies appearing in the
first 4 pages are colleted (as the list may be long, we stop at 4 pages). 
* Each page contains 50 movies. So, we would parse 50 * 4 * 22 == 4400 movies
* For those movies without a metascore rating, we skip saving it to our data.
* Here is an example page for 2017 movies
https://www.imdb.com/search/title/?release_date=2017&sort=num_votes,desc

2. How was this data collected?
* The IMDB scraper is borrowed from this link with small additions:
https://www.dataquest.io/blog/web-scraping-beautifulsoup/   
* We make multiple requests with varying years and page numbers. 
* We accumulate all the data, transform it to a dataframe, and save it.

3. How will we use this data in the course?
* We will use this data for demonstrating search for an information need.
* We will build a search engine that indexes this data and will be able
to respond to your search queries. 
* We use this data to demonstrate all the concepts and ideas leading up
the search engine such as boolean retrieval and ranked retrieval.
"""
# Read the movie review data
movie_dataset = pd.read_csv("data/imdb_movie_ratings/movie_ratings_2000_2022.csv")
print(movie_dataset)

# Data cleaning
print(movie_dataset["year"].unique())
print("(2005)"[-5:-1])
print(movie_dataset["year"].apply(lambda x: x[-5:-1]))
movie_dataset.loc[:, "year"] = movie_dataset["year"].apply(lambda x: x[-5:-1])
print(movie_dataset)
movie_dataset.to_csv(
    "data/imdb_movie_ratings/clean_movie_ratings_2000_2022.csv", index=False
)
