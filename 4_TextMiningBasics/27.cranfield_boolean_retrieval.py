import time
import pandas as pd
from cranfiled_data import CranDocuments, CranQueries, CranQueryReleventDocs
from boolen_retrieval_helper import TextPreProcessor
from ranking_metrics import compute_precision_and_recall


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

    def __init__(self, terms: set, cran_docs_df: pd.DataFrame) -> None:
        self.cran_docs_df = cran_docs_df
        self.doc_number_doc_name_lookup = self.create_doc_number_doc_name_lookup(
            cran_docs_df
        )
        self.doc_name_doc_number_lookup = {
            v: k for k, v in self.doc_number_doc_name_lookup.items()
        }
        self.postings_list = {t.lower(): [] for t in terms}
        self.postings_list = self.process_all_documents()

    def get_postings_list(self):
        return self.postings_list

    def create_doc_number_doc_name_lookup(self, cran_docs_df: pd.DataFrame):
        return {i: i for i in cran_docs_df["id"].values}

    def update_postings_list(self, document_name: str, document_string: str):
        doc_num = self.doc_name_doc_number_lookup[document_name.lower()]
        tokens = TextPreProcessor(document_string).get_tokens()
        for token in tokens:
            self.postings_list[token.lower()].append(doc_num)

    def sort_postings(self):
        for k in self.postings_list:
            v = self.postings_list[k]
            self.postings_list[k] = sorted(list(set(v)))

    def get_postings(self, token: str):
        if token.lower() in self.postings_list:
            return self.postings_list[token.lower()]
        else:
            return None

    def process_all_documents(self):
        st = time.time()
        for row in self.cran_docs_df.itertuples():
            self.update_postings_list(row.id, row.abstract)
        # mandatory sorting of postings
        self.sort_postings()
        print(f"Indexing all documents took: {time.time() - st:.2} seconds")
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
        title_terms = TextPreProcessor(row.title).get_tokens()
        for term in abstract_terms + title_terms:
            terms.add(term)
        doc_ids.add(row.id)
    return terms, doc_ids


def index_cran_data(cran_docs_df):
    terms, _ = get_all_terms_and_document_ids(cran_docs_df)
    print(cran_docs_df.columns)
    postings_list = PostingsList(terms, cran_docs_df)
    # p1 = postings_list.get_postings("shear")
    # print(p1)
    # p2 = postings_list.get_postings("heat")
    # print(p2)
    # result = intersect_postings_list(p1, p2)
    # print(result)
    return postings_list


def start_interactive_search_using_postings_index(postings_list):
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
                TextPreProcessor(token).get_tokens()[0]
                v1 = postings_list.get_postings(stack.pop())
                if not stack:
                    if v1 is not None:
                        result = v1
                        break
                    else:
                        break
                # and, or
                # operator
                # operand
                operator = stack.pop()
                v2 = postings_list.get_postings(stack.pop())
                if v1 is None or v2 is None:
                    break
                if operator == "and":
                    result = intersect_postings_list(v1, v2)
                elif operator == "or":
                    result = v1 + v2
                else:
                    print(f"{operator} operator not supported!")
                    break
                first_iter = False
            else:
                operator = stack.pop()
                v1 = postings_list.get_postings(stack.pop())
                if v1 is None:
                    break
                if operator == "and":
                    result = intersect_postings_list(v1, result)
                elif operator == "or":
                    result = v1 + result
                else:
                    print(f"{operator} operator not supported!")
                    break
        print("********** searh results **********")
        if result is not None:
            for doc_num in result:
                print(postings_list.doc_number_doc_name_lookup[doc_num])
        print("***********************************")


def evaluate_cran_queries(postings_list, cran_queries_df, operator, cran_qrels):
    # queries_to_process = 5
    results = []
    precision_sum = 0
    recall_sum = 0
    query_count = 0
    for row in cran_queries_df.itertuples():
        # if queries_to_process == 0:
        #     break
        # print(row)
        # print(f"Query: {row.query_text}")
        query_terms = TextPreProcessor(row.query_text).get_tokens()
        # query_terms = query_terms[:2]
        # print(f"Query after pre-processing: {query_terms}")
        if str(row.int_id) not in cran_qrels:
            print(
                f"!!!!!!!!!!!!! could not find query ID {str(row.int_id)} in cran_qrels !!!!!!!!!!!!!"
            )
            continue
        expected_docs = cran_qrels[str(row.int_id)]
        expected_docs_list = [list(entry.keys())[0] for entry in expected_docs]
        # print(f"Expected documents: {expected_docs_list}")
        result = []
        first_iter = True
        while query_terms:
            if first_iter:
                v1 = postings_list.get_postings(query_terms.pop())
                v2 = postings_list.get_postings(query_terms.pop())
                if v1 is None or v2 is None:
                    break
                if operator == "and":
                    result = intersect_postings_list(v1, v2)
                else:
                    result = v1 + v2
                first_iter = False
            else:
                v1 = postings_list.get_postings(query_terms.pop())
                if v1 is None:
                    break
                if operator == "and":
                    result = intersect_postings_list(v1, result)
                elif operator == "or":
                    result += v1
        # queries_to_process -= 1
        # print(f"Documents returned: {result}")
        p, r = compute_precision_and_recall(expected_docs_list, result)
        precision_sum += p
        recall_sum += r
        print(f"precision: {p}, recall: {r}")
        results.append(result)
        query_count += 1
        print("*********************************\n")

    print(f"Average precision: {precision_sum / query_count}")
    print(f"Average recall: {recall_sum / query_count}")

    return results


if __name__ == "__main__":
    cran_docs = CranDocuments(
        "/Users/pramodanantharam/Downloads/cran/cran.all.1400"
    ).get_all_docs()
    cran_docs_df = get_documents_df(cran_docs)
    print(cran_docs_df.shape)
    print(cran_docs_df)
    cran_queries = CranQueries(
        "/Users/pramodanantharam/Downloads/cran/cran.qry"
    ).get_all_queries()
    cran_queries_df = get_queries_df(cran_queries)
    print(cran_queries_df.shape)
    print(cran_queries_df)
    cran_qrels = CranQueryReleventDocs(
        "/Users/pramodanantharam/Downloads/cran/cranqrel"
    ).get_query_relevantdocs_map()
    postings_list = index_cran_data(cran_docs_df)
    # start_interactive_search_using_postings_index(postings_list)
    results = evaluate_cran_queries(postings_list, cran_queries_df, "or", cran_qrels)
    # print(results)
