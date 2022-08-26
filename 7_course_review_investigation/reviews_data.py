import os
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords
from tkinter.tix import Tree
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup


class ReviewData:
    def __init__(self, review_files_directory) -> None:
        self.review_files_directory = review_files_directory
        self.review_data = self.prepare_review_data()

    @property
    def data(self):
        return self.review_data.reset_index(drop=Tree)

    @property
    def positive_review_data(self):
        return self.review_data[self.review_data.rating > 3].reset_index(drop=True)

    @property
    def negative_review_data(self):
        return self.review_data[self.review_data.rating <= 3].reset_index(drop=True)

    def prepare_review_data(self):
        review_data_list = []
        for file in tqdm(os.listdir(self.review_files_directory)):
            if file.endswith("html"):
                url = os.path.join(self.review_files_directory, file)
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
                    rating = float(rating.text.split(" ")[1])
                    review_data_list.append(
                        {"rating": rating, "comment": comment.p.text}
                    )

        review_data = pd.DataFrame.from_dict(review_data_list)
        return review_data

    def generate_word_cloud(self, text, out_file_name="word_cloud"):
        # Generate a word cloud image
        wordcloud = WordCloud(
            stopwords=list(stopwords.words("english")),
            background_color="white",
            width=1800,
            height=1400,
            collocation_threshold=1,
        ).generate(text)
        # Display the generated image:
        # the matplotlib way:
        plt.figure(figsize=(14, 10))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        # plt.savefig(out_file_name, dpi=600)
        wordcloud.to_file(out_file_name)


if __name__ == "__main__":
    review_data = ReviewData("../data/html_review_files")
    print(review_data.data)
    print(review_data.positive_review_data)
    print(review_data.negative_review_data)
    review_data.data.to_csv("course_reviews.csv", index=False)
    review_data.generate_word_cloud(
        " ".join(list(review_data.data["comment"].values)),
        out_file_name="all_words.png",
    )
    review_data.generate_word_cloud(
        " ".join(list(review_data.positive_review_data["comment"].values)),
        out_file_name="positive_words.png",
    )
    review_data.generate_word_cloud(
        " ".join(list(review_data.negative_review_data["comment"].values)),
        out_file_name="negative_words.png",
    )
