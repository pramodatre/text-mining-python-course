# Datasets
Directory names containing datasets and their brief description.
## aclimdb
You may not see this directory when you clone this repository. Since this dataset is huge, checking in this data doesn't make sense. You will need to run the script `get_imdb_reviews_data.sh` to get this data. This script will download the
Large Movie Review Dataset dataset files from http://ai.stanford.edu/~amaas/data/sentiment/
You will be able to see a directory named `aclimdb` after you run the above script. If you cannot run the scrip, please refer to the videos where I will show the process to manually download this dataset.

## html_reviews_file
Udemy reviews of Text Mining courses. This dataset will be used in the course to demonstrate the value of text mining for decision making. I used the insights from Text Mining done on these reviews to carefully craft this course. Specifically, I looked at student likes/dislikes and their pain-points from reviews to make sure I address when creating this course.

## imdb_movie_ratings
Contains data for around top-200 movies with highest number of votes from year 2000 to 2022 are collected for this dataset.

# Scripts
## get_imdb_reviews_data.sh
This is a shell script that you can run on a linux/MacOS machine to download the Large Movie Review Dataset. If you are using Windows OS, please follow the manual download instructions in the video lectures.

## imdb_scraper.py
Contains code to scrape IMDB movie ratings and short descriptions from IMDB website. Around top-200 movies with highest number of votes from year 2000 to 2022 are collected for this dataset.