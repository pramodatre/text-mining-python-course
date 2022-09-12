# 1. Simple output example
print("Hello World!")

# 2. Example Input from user
name = input("Enter you name:")
print(name)

# 3. Output formatting
# 3a. Formatted String Literals
DAY_OF_WEEK = "Weekend"
print("You entered: ", name)
print(f"You entered {name} and today is a {DAY_OF_WEEK}")

# 3b. String format() method
print("You entered {} and today is a {}".format(name, DAY_OF_WEEK))

# File as input
# data/imdb_movie_ratings/movie_ratings_2000_2022.csv"
with open("data/imdb_movie_ratings/movie_ratings_2000_2022.csv") as f:
    lines = f.readlines()
    print(lines)
