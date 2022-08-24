import re
import requests
import os
from bs4 import BeautifulSoup

review_file_directory = "./html_review_files"

for file in os.listdir(review_file_directory):
    if file.endswith("html"):
        url = os.path.join(review_file_directory, file)
        page = open(url)
        soup = BeautifulSoup(page.read(), features="html.parser")

        reviews = soup.find_all(
            "div", class_="individual-review--individual-review-content--en4c7"
        )
        print(f"Total reviews: {len(reviews)}")
        for review in reviews:
            # print(review)
            rating = review.find("span", class_="udlite-sr-only")
            comment = review.find(
                "div", attrs={"data-purpose": {"review-comment-content"}}
            )
            print(rating.text)
            print(comment.p.text)
            print("--")
