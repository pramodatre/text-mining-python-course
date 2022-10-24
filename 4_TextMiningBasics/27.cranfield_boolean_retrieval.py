import time
import pandas as pd
from cranfiled_data import Documents, Queries, QueryReleventDocs
from boolen_retrieval_helper import TextPreProcessor


class PostingsList:
    """
    This index contains two parts:
    (1) Dictionary containing terms
    (2) Postings containing documents in which the terms occur sorted by document-ID
    For example:
    crash -> [94, 155, 238, 557, 930, 947]
    island -> [2, 48, 94, 100]
    ...

    When the index is too large to hold in memory, a sorted list of terms
    are stored in memory and each points to the postings stored on disk.
    """

    def __init__(
        self, terms: set, document_names: set, cran_docs_df: pd.DataFrame
    ) -> None:
        self.cran_docs_df = cran_docs_df
        self.doc_number_doc_name_lookup = self.create_doc_number_doc_name_lookup(
            document_names
        )
        self.doc_name_doc_number_lookup = {
            v: k for k, v in self.doc_number_doc_name_lookup.items()
        }
        self.postings_list = {t.lower(): [] for t in terms}
        self.postings_list = self.process_all_documents()

    def get_postings_list(self):
        return self.postings_list

    def create_doc_number_doc_name_lookup(self, document_names: set):
        doc_number_doc_name_lookup = {}
        for i, doc_name in enumerate(document_names):
            doc_number_doc_name_lookup[i] = doc_name.lower()
        return doc_number_doc_name_lookup

    def update_postings_list(self, document_name: str, document_string: str):
        doc_num = self.doc_name_doc_number_lookup[document_name.lower()]
        tokens = TextPreProcessor(document_string).get_tokens()
        for token in tokens:
            self.postings_list[token.lower()].append(doc_num)

    def sort_postings(self):
        for k in self.postings_list:
            v = self.postings_list[k]
            self.postings_list[k] = sorted(v)

    def get_postings(self, token: str):
        if token.lower() in self.postings_list:
            return self.postings_list[token.lower()]
        else:
            return None

    def process_all_documents(self):
        st = time.time()
        for row in self.cran_docs_df.itertuples():
            self.update_postings_list(row.id, row.abstract)
        print(f"Indexing all movies took: {time.time() - st:.2} seconds")
        # mandatory sorting of postings
        self.sort_postings()
        return self.postings_list


def intersect_postings_list(p1: list, p2: list):
    """Implementation of the algorithm for intersection of two postings
    list. page 11, Figure 1.6 Algorithm for the intersection of two postings lists p1 and p2.

    Args:
        p1 (list): 1st postings
        p2 (list): 2nd postings
    """
    i = 0
    j = 0
    result = []
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:
            result.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            i += 1
        elif p1[i] > p2[j]:
            j += 1
    return result


def get_documents_df(docs: list):
    """Accepts a list containing Document type

    Args:
        docs (list): Containing Document type

    Returns:
        pandas.DataFrame: Containing all documents
    """
    docs_dict_list = []
    for doc in docs:
        # print(vars(doc))
        docs_dict_list.append(vars(doc))
    return pd.DataFrame(docs_dict_list)


def get_queries_df(queries: list):
    """Accepts a list containng Query type

    Args:
        queries (list): Containing Query type

    Returns:
        pd.DataFrame: Containing all queries
    """
    queries_dict_list = []
    for query in queries:
        queries_dict_list.append(vars(query))

    return pd.DataFrame(queries_dict_list)


def get_all_terms_and_document_ids(cran_dataset):
    terms = set()
    doc_ids = set()
    for row in cran_dataset.itertuples():
        abstract_terms = TextPreProcessor(row.abstract).get_tokens()
        for term in abstract_terms:
            terms.add(term)
        doc_ids.add(row.id)
    return terms, doc_ids


def index_cran_data(cran_docs_df):
    terms, doc_ids = get_all_terms_and_document_ids(cran_docs_df)
    postings_list = PostingsList(terms, doc_ids, cran_docs_df)
    p1 = postings_list.get_postings("shear")
    print(p1)
    p2 = postings_list.get_postings("heat")
    print(p2)
    result = intersect_postings_list(p1, p2)
    print(result)


if __name__ == "__main__":
    cran_docs = Documents(
        "/Users/pramodanantharam/Downloads/cran/cran.all.1400"
    ).get_all_docs()
    cran_docs_df = get_documents_df(cran_docs)
    print(cran_docs_df.shape)
    print(cran_docs_df)
    cran_queries = Queries(
        "/Users/pramodanantharam/Downloads/cran/cran.qry"
    ).get_all_queries()
    cran_queries_df = get_queries_df(cran_queries)
    print(cran_queries_df.shape)
    print(cran_queries_df)
    cran_qrels = QueryReleventDocs(
        "/Users/pramodanantharam/Downloads/cran/cranqrel"
    ).get_query_relevantdocs_map()
    index_cran_data(cran_docs_df)
