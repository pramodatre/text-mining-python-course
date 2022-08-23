import re
import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://www.udemy.com/course/applied-text-mining-and-sentiment-analysis-with-python/"
)

soup = BeautifulSoup(response.text, "html.parser")
print(soup.title)

# <div data-purpose="landing-page-review-list">
# div class="reviews-section--review-container--3F3NE"
# udlite-text-sm individual-review--individual-review__comment--2o94n
# reviews-section--review-container--3F3NE
# reviews = soup.findAll("div", class_="component-margin")
# print(reviews.descendants)
# reviews = soup.find_all("div")
# print(reviews)
# for title in reviews:
#     print(title.descendants)
#     for child in title.descendants:
#         print(
#             child.findAll(
#                 "div",
#                 class_="udlite-text-sm individual-review--individual-review__comment--2o94n",
#             )
#         )

reviews = soup.findAll(
    "div",
    class_="component-margin",
    recursive=True,
)

print(reviews)

for item in reviews:
    reviews = item.findAll("span", id="reviews")
    if reviews:
        print(reviews)
