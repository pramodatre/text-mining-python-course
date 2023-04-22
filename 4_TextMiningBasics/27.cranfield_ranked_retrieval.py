import numpy as np
from cranfiled_data import CranDocuments, CranQueries, CranQueryReleventDocs
from boolen_retrieval_helper import TextPreProcessor
from vector_space_model_demo import DocStats, DocStatsScikit
from ranking_metrics import (
    mean_average_precision_at_k,
    compute_precision_and_recall,
)


def get_documents_in_a_dict(cran_docs: CranDocuments):
    """Collect all abstracts (documents we are indexing)
    in a list and return them.

    Args:
        cran_docs (CranDocuments): List containing instance
            of cranfield_data.Document object.

    Returns:
        list: Containing abstracts/documents to be indexed.
    """
    docs = {}
    for doc in cran_docs:
        docs[doc.id] = doc.abstract

    return docs


def launch_search_engine(doc_stats: DocStats):
    while True:
        query = input("Enter your search query: ")
        if query == "":
            break
        query = " ".join(TextPreProcessor(query).get_tokens())
        q = doc_stats.get_unit_vector_for_text(query)
        doc_score_map = {}
        for doc_id in doc_stats.document_vector_map:
            score = np.dot(q, doc_stats.document_vector_map[doc_id])
            doc_score_map[doc_id] = score
        # Display top-k results
        k = 20
        sorted_docs = dict(
            sorted(doc_score_map.items(), key=lambda item: item[1], reverse=True)
        )
        for doc_id in sorted_docs:
            print(doc_id)
            k -= 1
            if k == 0:
                break


def evaluate_MAP_at_k_on_cranfield_data(
    doc_stats: DocStats,
    cran_queries: CranQueries,
    cran_qrels: CranQueryReleventDocs,
    k=10,
):
    rel_docs_list = []
    retrieved_docs_list = []
    for query in cran_queries:
        q = " ".join(TextPreProcessor(query.query_text).get_tokens())
        q_unit = doc_stats.get_unit_vector_for_text(q)
        doc_score_map = {}
        for doc_id in doc_stats.document_vector_map:
            score = np.dot(q_unit, doc_stats.document_vector_map[doc_id])
            doc_score_map[doc_id] = score
        sorted_docs = dict(
            sorted(doc_score_map.items(), key=lambda item: item[1], reverse=True)
        )
        sorted_doc_ids = [str(doc_id) for doc_id in sorted_docs]
        if str(query.int_id) in cran_qrels:
            rel_docs = cran_qrels[str(query.int_id)]
            rel_doc_ids = [list(k.keys())[0] for k in rel_docs]
            print(f"Query ID: {str(query.int_id)}")
            print(rel_doc_ids)
            print(sorted_doc_ids[:k])
            print("***")
            rel_docs_list.append(rel_doc_ids)
            retrieved_docs_list.append(sorted_doc_ids[:k])

    mAP = mean_average_precision_at_k(rel_docs_list, retrieved_docs_list)
    print(f"MAP@{k} = {mAP}")


def evaluate_precision_recall_cranfiled_data(
    doc_stats: DocStats,
    cran_queries: CranQueries,
    cran_qrels: CranQueryReleventDocs,
    k=10,
):
    precisions = []
    recalls = []
    for query in cran_queries:
        q = " ".join(TextPreProcessor(query.query_text).get_tokens())
        q_unit = doc_stats.get_unit_vector_for_text(q)
        doc_score_map = {}
        for doc_id in doc_stats.document_vector_map:
            score = np.dot(q_unit, doc_stats.document_vector_map[doc_id])
            doc_score_map[doc_id] = score
        sorted_docs = dict(
            sorted(doc_score_map.items(), key=lambda item: item[1], reverse=True)
        )
        sorted_doc_ids = [str(doc_id) for doc_id in sorted_docs]
        if str(query.int_id) in cran_qrels:
            rel_docs = cran_qrels[str(query.int_id)]
            rel_doc_ids = [list(k.keys())[0] for k in rel_docs]
            # print(f"Query ID: {str(query.int_id)}")
            # print(rel_doc_ids)
            # print(sorted_doc_ids[:k])
            # print("***")
            p, r = compute_precision_and_recall(rel_doc_ids, sorted_doc_ids[:k])
            precisions.append(p)
            recalls.append(r)
    print("Average precision: ", np.mean(precisions))
    print("Average recall: ", np.mean(recalls))


if __name__ == "__main__":
    cran_docs = CranDocuments().get_all_docs()
    cran_queries = CranQueries().get_all_queries()
    cran_qrels = CranQueryReleventDocs().get_query_relevantdocs_map()
    # print(cran_qrels)
    docs = get_documents_in_a_dict(cran_docs)
    # print(len(docs))
    doc_stats = DocStats(docs)
    # doc_stats = DocStatsScikit(docs)
    print("# of documents: ", doc_stats.get_number_of_docs())
    print("# of terms in the vocabulary: ", len(doc_stats.vocabulary))
    # launch_search_engine(doc_stats)
    evaluate_MAP_at_k_on_cranfield_data(doc_stats, cran_queries, cran_qrels)
    evaluate_precision_recall_cranfiled_data(doc_stats, cran_queries, cran_qrels)
