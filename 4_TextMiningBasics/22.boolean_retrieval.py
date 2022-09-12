import time
import pandas as pd
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


class TermDocumentIncidenceMatrix:
    def __init__(self, terms: set, document_names: set) -> None:
        self.terms = terms
        self.terms = [term.lower() for term in self.terms]
        self.document_names = document_names
        self.document_names = [
            document_name.lower() for document_name in self.document_names
        ]
        self.term_doc_incidence_matrix = pd.DataFrame(
            index=self.terms, columns=self.document_names, dtype=np.int32
        )
        self.term_doc_incidence_matrix = self.term_doc_incidence_matrix.fillna(
            0
        ).astype("int64")

    def get_term_vector(self, term: str):
        term = TextPreProcessor(term).get_tokens()[0]
        if term in self.term_doc_incidence_matrix.index:
            return self.term_doc_incidence_matrix.loc[term]
        else:
            return None

    def get_document_vector(self, document_name: str):
        if document_name.lower() in self.term_doc_incidence_matrix.columns:
            return self.term_doc_incidence_matrix[document_name]
        else:
            return None

    def update_term_doc_incidence_matrix(
        self, document_name: str, document_string: str
    ):
        term_vector = pd.Series(index=self.terms, dtype=np.int32)
        term_vector = term_vector.fillna(0).astype("int64")
        tokens = TextPreProcessor(document_string).get_tokens()
        for token in tokens:
            term_vector[token.lower()] = 1
        self.term_doc_incidence_matrix[document_name.lower()] = term_vector

    def print_info_of_term_doc_incidence_matrix(self):
        print(self.term_doc_incidence_matrix.info())
        print(self.term_doc_incidence_matrix)


def get_all_terms_and_movie_names(movie_dataset):
    terms = set()
    movie_names = set()
    unique_movies = movie_dataset.drop_duplicates(subset=["movie"])
    for row in unique_movies.itertuples():
        movie_desc_terms = TextPreProcessor(row.description).get_tokens()
        for term in movie_desc_terms:
            terms.add(term)
        movie_names.add(row.movie)
    return terms, movie_names


def process_all_documents():
    movie_dataset = pd.read_csv(
        "data/imdb_movie_ratings/clean_movie_ratings_2000_2022.csv"
    )
    print(movie_dataset)
    # (1) Build term vocabulary and collect all document/document names
    terms, movie_names = get_all_terms_and_movie_names(movie_dataset)
    # (2) Build the index -- i.e., term-document incidence matrix
    tdi_matrix = TermDocumentIncidenceMatrix(terms, movie_names)
    tdi_matrix.print_info_of_term_doc_incidence_matrix()
    st = time.time()
    for row in movie_dataset.itertuples():
        tdi_matrix.update_term_doc_incidence_matrix(row.movie, row.description)
    print(f"Indexing all movies took: {time.time() - st:.2} seconds")
    tdi_matrix.print_info_of_term_doc_incidence_matrix()
    doc_vec = tdi_matrix.get_document_vector("cast away")
    print(sum(doc_vec))
    return tdi_matrix


def start_interactive_search(tdi_matrix):
    while True:
        query = input("Enter the search query: ")
        print(f"your query: {query}")
        if not query:
            break
        print(query.split(" "))
        stack = []
        # island and crash and fedex
        for token in query.split(" "):
            stack.append(token)
        print(stack)
        result = None
        first_iter = True
        while stack:
            if first_iter:
                # TextPreProcessor(token).get_tokens()[0]
                v1 = tdi_matrix.get_term_vector(stack.pop())
                if not stack:
                    if v1 is not None:
                        result = v1.values
                        break
                    else:
                        break
                # and, or
                # operator
                # operand
                operator = stack.pop()
                v2 = tdi_matrix.get_term_vector(stack.pop())
                if v1 is None or v2 is None:
                    break
                if operator == "and":
                    result = v1.values & v2.values
                elif operator == "or":
                    result = v1.values | v2.values
                else:
                    print(f"{operator} operator not supported!")
                    break
                first_iter = False
            else:
                operator = stack.pop()
                v1 = tdi_matrix.get_term_vector(stack.pop())
                if v1 is None:
                    break
                if operator == "and":
                    result = v1.values & result
                elif operator == "or":
                    result = v1.values | result
                else:
                    print(f"{operator} operator not supported!")
                    break
        print("********** searh results **********")
        if result is not None:
            idxes = np.where(result == 1)[0]
            for idx in idxes:
                print(tdi_matrix.document_names[idx])
        print("***********************************")


class TextPreProcessor:
    def __init__(self, text) -> None:
        self.tokens = self.tokenize(text)
        self.tokens = self.remove_stopwords(self.tokens)
        # self.tokens = self.apply_stemming(self.tokens)
        self.tokens = self.apply_lemmatization(self.tokens)

    def get_tokens(self):
        return self.tokens

    def tokenize(self, text):
        """
        For example (from IR book, manning, raghavan, schutze):
        "Mr. O’Neill thinks that the boys’ stories about Chile’s capital aren’t amusing."

        Which of these tokens should we index for O’Neill?
        neill
        oneill
        o'neill
        o' neill
        o neill

        Which of these tokens should we index for aren’t?
        aren’t
        arent
        are n't
        aren t

        Key insight is here, we should use the same token extractor for both: (1) text we index and (2) the query so that terms map to the same normalized form.

        For example, say we decide to use "o neill" as the token we want to index. At query time, if the user enters "O’Neill" as search term, we should tokenize it to "o neill" -- this is the only way we can retrieve relevant documents. If "O’Neill" in the query is mapped to "o'neill" then this term is not even present in our index (assuming that we have indexed only two documents above). We will end up returning no documents as relevant documents.

            Args:
                text (str): Text to be tokenized

            Returns:
                list: Containing tokes
        """
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens if token.isalpha()]
        return tokens

    def remove_stopwords(self, tokens):
        """Removes common stop words using the NLTK
        english stop words.

        Args:
            tokens (list): Containing input tokens

        Returns:
            list: Containing tokens after excluding tokes
                    that are in the NLTK stop word set
        """
        stop_words = set(stopwords.words("english"))
        return [token for token in tokens if token not in stop_words]

    def apply_stemming(self, tokens):
        """
        For example (from IR book, manning, raghavan, schutze):

        operate operating operates operation operative operatives operational => oper

        operational AND research
        operating AND system
        operative AND dentistry

        Args:
            tokens (_type_): _description_
        """
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in tokens]

    def apply_lemmatization(self, tokens):
        """
        operative operatives => operative

        operational AND research
        operating AND system

        Args:
            tokens (_type_): _description_
        """
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(token) for token in tokens]


if __name__ == "__main__":
    movie_description_1 = "A FedEx executive undergoes a physical and emotional transformation after crash landing on a deserted island."
    movie_description_2 = "On vacation in Thailand, Richard sets out for an island rumored to be a solitary beach paradise."
    sample_text = "Mr. O’Neill thinks that the boys’ stories about Chile’s capital aren’t amusing."
    print(TextPreProcessor(movie_description_1).get_tokens())
    print(TextPreProcessor(movie_description_2).get_tokens())
    print(TextPreProcessor(sample_text).get_tokens())
    # Process all documents in the movie rating dataset
    # Each movie description is a document for us
    tdi_matrix = process_all_documents()
    island = tdi_matrix.get_term_vector("island")
    crash = tdi_matrix.get_term_vector("crash")
    result = island.values & crash.values
    idxes = np.where(result == 1)[0]
    print(idxes)
    for idx in idxes:
        print(tdi_matrix.document_names[idx])
    start_interactive_search(tdi_matrix)
    # print(TextPreProcessor("crash").get_tokens()[0])
