# Code Reference: https://www.kaggle.com/code/nandeshwar/mean-average-precision-map-k-metric-explained-code/notebook
import numpy as np


def compute_precision_and_recall(expected_docs: list, retrieved_docs: list):
    expected_docs = set(expected_docs)
    retrieved_docs = set(retrieved_docs)
    relevant_docs_retrieved = len(retrieved_docs.intersection(expected_docs))
    total_retrieved_docs = len(retrieved_docs) + 1e-4
    total_relevant_docs = len(expected_docs) + 1e-4
    precision = relevant_docs_retrieved / total_retrieved_docs
    recall = relevant_docs_retrieved / total_relevant_docs
    return precision, recall


def average_precision_at_k(actual: list, predicted: list, k=5) -> float:
    """Computes average precision at k
    This metric is suitable for evaluating set based retrieval.

    Args:
        actual (list): Expected search results
        predicted (list): Predicted search results
        k (int, optional): k values on the top
            of the returned search results to consider
            for evaluation. Defaults to 5.

    Returns:
        _type_: _description_
    """
    if not actual:
        return 0.0
    # Truncate predictions to match k
    predicted = predicted[:k]

    score = 0.0
    hits = 0.0

    for i, p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            hits += 1
            score += hits / (i + 1.0)

    return score / min(len(actual), k)


def mean_average_precision_at_k(actual: list, predicted: list, k=5) -> float:
    """Computes mean average precision at k (MAP@k)
    This metric is suitable for evaluating set based retrieval.
    MAP@k is measured for a set of queries or multiple
    search results served for multiple users of a search
    system. MAP@k provides a single score for the search
    system.

    Args:
        actual (list): List containing lists of
            expected search results for each query/user.
        predicted (list): List of lists where each list is
            the predicted
        k (int, optional): _description_. Defaults to 5.

    Returns:
        _type_: _description_
    """
    return np.mean([average_precision_at_k(g, p) for g, p in zip(actual, predicted)])


def cumulative_gain(rel_score_of_pred_items: list) -> float:
    """Cumulative gain for a list of recommended items using
    the relevance judgement score. Relevance judgement
    indicates/quantifies the spectrum of
    highly-relevant docs -> marginally relevant ->
    irrelevant documents.

    Args:
        rel_score_of_pred_items (list): Containing relevance
            score for each item in the recommended list

    Returns:
        float: cumulative gain
    """
    return np.sum(rel_score_of_pred_items)


def discounted_cumulative_gain(rel_score_of_pred_items: list) -> float:
    """Discounted cumulative gain implementation which
    is an improvement over cumulative gain. Rewards relevant
    documents at the top of the recommended list. This
    is especially important in evaluating recommender/Information
    Retrieval systems since we want the items on top of the
    list to be highly relevant.

    Args:
        rel_score_of_pred_items (list): Containing relevance
            score for each item in the recommended list

    Returns:
        float: discounted cumulative gain (DCG)
    """
    dcg = 0.0
    for i, rel_score in enumerate(rel_score_of_pred_items, 1):
        dcg += rel_score / np.log2(i + 1)

    return dcg


def normalized_discounted_cumulative_gain(
    rel_score_of_pred_items: list, ideal_real_score_of_pred_items: list
) -> float:
    """Normalized discounted cumulative gain (NDCG) implementation
    which is an improvement over DCG. DCG varies widely depending
    on the number of search results returned. A normalized score
    will be easier to compare. NDCG is a good metric for quantifying
    quality of a ranked retrieval system.

    Args:
        rel_score_of_pred_items (list): _description_

    Returns:
        float: _description_
    """
    dcg = discounted_cumulative_gain(rel_score_of_pred_items)
    idcg = discounted_cumulative_gain(ideal_real_score_of_pred_items)

    return dcg / idcg


if __name__ == "__main__":
    # Test metric implementations
    # Average Precision and Mean Average Precision
    # Subset of relevant documents for
    # Query 1 of the cranfiled dataset
    actual_rel_docs = [15, 14, 13, 102, 51, 12, 31, 29, 184]
    # actual_rel_scores used for ranking metrics such as NDCG
    # We have subtracted the relevance score from 5
    actual_rel_scores = [1, 1, 1, 2, 2, 2, 3, 3, 3]
    # Say, you are comparing two recommendations
    # Recommendation 1 has no relevant docs at the top of the list
    rec_1 = [23, 34, 0, 184, 29, 12, 11]
    # Recommendation 2 has some relevant docs on top of the list
    rec_2 = [184, 29, 12, 23, 34, 10, 11]
    print("*** Average precision and Mean average precition ***")
    print(
        "Average precision @ k for rec_1: ",
        average_precision_at_k(actual_rel_docs, rec_1, k=5),
    )
    print(
        "Average precision @ k for rec_2: ",
        average_precision_at_k(actual_rel_docs, rec_2, k=5),
    )
    # Mean Average precision is used for multiple recommendations
    # served for multiple users of the SAME SEARCH SYSTEM/ENGINE
    # For testing purposes, let's pretend that that rec_1 and rec_2
    # are the recommendations provided by our search engine
    # for two search queries by two users.
    print(
        "Mean Average Precision @ k for two search results: ",
        mean_average_precision_at_k([actual_rel_docs, actual_rel_docs], [rec_1, rec_2]),
    )

    # NDCG -- Normalized Discounted Cumulative Gain
    # Cumulative Gain
    # These are relevance scores obtained from actual_rel_scores
    # for each document id in rec_1 and rec_2
    print("*** NDCG -- Normalized Discounted Cumulative Gain ***")
    # Cumulative gain
    rec_1 = [0, 0, 0, 3, 3, 2, 0]
    rec_2 = [3, 3, 2, 0, 0, 0, 0]
    print("Cumulative Gain for rec_1: ", cumulative_gain(rec_1))
    print("Cumulative Gain for rec_2: ", cumulative_gain(rec_2))
    # Discounted cumulative gain
    dcg_rec_1 = discounted_cumulative_gain(rec_1)
    dcg_rec_2 = discounted_cumulative_gain(rec_2)
    print(f"Discounted Cumulative Gain (DCG) for rec_1: {dcg_rec_1:.3}")
    print(f"Discounted Cumulative Gain (DCG) for rec_2: {dcg_rec_2:.3}")
    # Normalized DGC
    ideal_dcg = discounted_cumulative_gain(actual_rel_scores)
    ndcg_rec_1 = dcg_rec_1 / ideal_dcg
    ndcg_rec_2 = dcg_rec_2 / ideal_dcg
    print(f"Normalized Discounted Cumulative Gain (NDCG) for rec_1: {ndcg_rec_1:.3}")
    print(f"Normalized Discounted Cumulative Gain (NDCG) for rec_2: {ndcg_rec_2:.3}")
    # We can wrap NDCG computation into a single method
    ndcg_rec_1 = normalized_discounted_cumulative_gain(rec_1, actual_rel_scores)
    ndcg_rec_2 = normalized_discounted_cumulative_gain(rec_2, actual_rel_scores)
    print(f"NDCG from the wrapper method for rec_1: {ndcg_rec_1:.3}")
    print(f"NDCG from the wrapper method for rec_2: {ndcg_rec_2:.3}")
