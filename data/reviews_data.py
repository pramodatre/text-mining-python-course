import re
import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://www.udemy.com/course/applied-text-mining-and-sentiment-analysis-with-python/"
)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.title)

# soup = BeautifulSoup(response.text, "lxml")
# reviews = soup.findAll(
#     {
#         "div": {
#             "class": "udlite-text-sm individual-review--individual-review__comment--2o94n"
#         }
#     }
# )

# print(len(reviews))

# for review in reviews:
#     print(review.text)
# soup = BeautifulSoup(response.text, "html.parser")
# print(soup.title)

# result = soup.select(
#     "div.paid-course-landing-page__body div.course-landing-page__main-content div.component-margin"
# )
# print(result[10])
# print(len(result))

# for res in result:
#     r = soup.select("div div h2.udlite-heading-xl reviews-section--title--sOfZR")
#     print(r)

# result = soup.findAll(
#     "div",
#     attrs={"class": "component-margin"},
# )
# count = 1
# for div in result:
#     if count == 9:
#         print(div.div)
#         for d in div.div:
#             print(d)
#     count += 1


# for div in soup.findAll(
#     "div",
#     attrs={"class": "component-margin"},
# ):
#     # print(type(div))
#     # print(type(div.div.div))
#     ratings_and_reviews = div.div.div
#     # print(ratings_and_reviews)
#     for tag in ratings_and_reviews:
#         print(tag)


# divs = soup.html.find_all("div", recursive=True)
# for div in divs:
#     print(div.text)

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

# reviews = soup.findAll(
#     "div",
#     class_="component-margin",
#     recursive=True,
# )

# print(reviews)

# for item in reviews:
#     reviews = item.findAll("span", id="reviews")
#     reviews = item.findAll("div", class_="reviews-section--review-container--3F3NE")
#     print(reviews)
#     if reviews:
#         print(reviews)
#         for item in reviews:
#             review_container = item.findAll(
#                 "div", class_="reviews-section--review-container--3F3NE"
#             )
#             print(review_container)
