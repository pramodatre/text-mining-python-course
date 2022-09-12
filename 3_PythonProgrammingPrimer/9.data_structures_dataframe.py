# Make sure Pandas library is installed
# pip install pandas

# Pandas Series
# It's a 1-D data structure with Index and data items
import pandas as pd

s = pd.Series(data=[1, 2, 3, 4, 5, 6], index=["a", "b", "c", "d", "e", "f"])
print(s)

# In simple terms, a DataFrame is like a table
# (think of Excel sheet) containing data. Each
# row has an index and each column has a name. Each
# column in a DataFrame is a Series data structure.

# Create a DataFrame
# Empty DataFrame
df = pd.DataFrame()
print(df)
print(df.empty)
# From Series
a = pd.Series(data=[1, 2, 3, 4, 5, 6])
b = pd.Series(data=[33, 4, 44, 55, 66, 77])
df = pd.DataFrame({"a": a, "b": b})
print(df)

# From a dictionary
a = []
for i in range(0, 7):
    a.append({"a": i, "b": i ** 2})
df = pd.DataFrame.from_dict(a)
print(df)

# Reading from a file data/imdb_movie_ratings/movie_ratings_2000_2022.csv"
# df = pd.read_csv("data/imdb_movie_ratings/movie_ratings_2000_2022.csv")
# print(df.columns)

# Selecting data from a DataFrame
# Select a column
print(df["b"])
# Select a row by index
print(df.iloc[3])
# Select a row by location (row number)
print(df.loc[2])
# Add index to a DataFrame
print(df)
df = df.set_index("b")
print(df)
# Add a column to the DataFrame
df["c"] = [1, 2, 3, 4, 5, 6, 7]
print(df)

# Reset index of a DataFrame
df = df.reset_index()
print(df)

# Apply a funtion to a column of a DataFrame
df["c_squared"] = df["c"].apply(lambda x: x ** 2)
print(df)

# Iterating over a DataFrame
for row in df.itertuples():
    print(row.c_squared)

for row in df.iterrows():
    print(row)

# Saving DataFrame to a File
df.to_csv("df_save_file.csv", index=False)
