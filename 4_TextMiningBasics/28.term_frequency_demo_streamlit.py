import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
from cranfiled_data import Documents, Queries, QueryReleventDocs
from boolen_retrieval_helper import TextPreProcessor


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

"""
# Build Text Mining Applications with Live-Coding in Python
This demo script is part of the Udemy course on `Build Text Mining Applications with Live-Coding in Python`. We will take a hands-on approach to understand term freqency (tf), inverse document frequency (idf), and tf-idf weighing.

## Dataset
We will use the cranfield dataset to understand the basics ideas in a hands-on way. Cranfield dataset contains three files:
* cran.all.1400: Contains all the abstracts of technical articles in the domain of aerospace engineering
* cran.qry: Contains queries for which experts have evaluated relevance
* cranqrel: Contains relevant documents for queries in cran.qry; not all quries in cran.qry have a corresponding entry in cranqrel.
"""
st.write("cran.all.1400")
st.write(cran_docs_df.head())

st.write("cran.qry")
st.write(cran_queries_df.head())

"""
cranqrel is a dictionary containing query ID from cran.qry as key and value is a list of dictionaries containing relevant document ID and corresponding relevance score (score ranges from 1 to 4 indicating highly relevant and marginally relevant respectively). A score of [-1 indicates that the document is irrelevant](https://ir-datasets.com/cranfield.html). So, we can ignore this entry for our evaluation purpose.
"""
keys = list(cran_qrels.keys())
st.write(
    f"Here are the relevant documents and their corresponding relevance score for query {keys[0]}:"
)
st.text(cran_qrels[keys[0]])

"""
## Document selection
"""
doc_id = st.selectbox(
    label="Select document to compute term frequency, inverse document frequency, and tf-idf score for each term in the document: ",
    options=cran_docs_df["id"],
)
doc_row = cran_docs_df[cran_docs_df["id"] == doc_id]
doc_title = doc_row["title"].values[0]
doc_abstract = doc_row["abstract"].values[0]

st.write(f"Title: {doc_title}")
st.write(f"Abstract: {doc_abstract}")

"""
## Term frequency (tf)
In the boolean model, we relied on the presene of a term in a document as our matching criteria. Clearly, this did not go well when there were a lot of matches. We would like to quantify a degree of match so that we can rank order the document by relevance. We can imagine that a document containing frequent mention of a query term should be ranked higher for the query term. We can assign weight to a term given its occurrence in a document -- we call this the term frequency. Term frequency is denoted as $tf_{t, d}$ where $tf_{t, d}$ is the term frequency for the term $t$ in the document $d$.

Here, you can select a document from the cranfiled dataset. The title, abstract, and the computed term frequencies are displayed for the selected document.
"""


def term_frequency(document: str) -> dict:
    # st.write(f"document: {document}")
    terms = TextPreProcessor(document).get_tokens()
    # st.write(f"pre-processed document: {terms}")
    return dict(Counter(terms))


tfs = term_frequency(doc_abstract)
st.text(tfs)

"""
There are certain limitations of using term frequency alone for ranking:
* Some terms occur a lot in documents but they are of no informational value, e.g., stop-words
* Some domain specific terms may occur a lot across documents which is of low value to distinguish documents, e.g., airplane may occur quite frequently across documents related to aeronautical engineering

To address these limitations, we will have to factor in the informational value of a term, i.e., its ability to distinguish between documents to serve a query term (or information need).

## Inverse document frequency (idf)
One way to address the limitation of term frequency is to scale down the term frequency weight by another term that determines the ability to distinguish between documents for a specified information need (query). We have two options:
* Use collection frequency of a term as a proxy for it's ability to distinguish between documents. The idea is a term that occurs in a lot of documents may not be useful to distinguish between documents to serve an information need.
* Use document frequency of a term as a proxy -- document frequency of a term is defined as the total number of documents in the collection that has the term

Since we serve documents for an information need (query), using document level statistic may be appropriate. So, we will use the document frequency to scale down the term frequency. We define the inverse document frequency.
"""
st.latex(
    r"""
         idf_{t} = log \frac{N}{df_{t}}
         """
)
"""
$idf_{t}$ of a rate term will be higher compared to to terms that occur across all documents.
"""

# TODO: create a data structure that has document to term mapping document1: {term1, ... , termN}


@st.cache
def document_terms_lookup(df: pd.DataFrame) -> dict:
    document_terms_map = {}
    for row in df.itertuples():
        terms = TextPreProcessor(row.abstract).get_tokens()
        document_terms_map[row.id] = set(terms)

    return document_terms_map


@st.cache
def inverse_document_frequency(term: str) -> float:
    document_terms_map = document_terms_lookup(cran_docs_df)
    docs_containing_term = []
    total_docs = len(list(document_terms_map.keys()))
    for doc_id in document_terms_map:
        if term in document_terms_map[doc_id]:
            docs_containing_term.append(doc_id)

    return np.log(total_docs / len(docs_containing_term))


def compute_idf(text: str) -> dict:
    idfs = {}
    terms = TextPreProcessor(text).get_tokens()
    for term in terms:
        idfs[term] = inverse_document_frequency(term)

    return idfs


idfs = compute_idf(doc_abstract)
st.text(idfs)

""" 
## Tf-idf weighting
We will combine term frequency and inverse document frequency for each term in each document. tf-idf assigns weight to a term $t$ in document $d$ given by
"""
st.latex(
    r"""
         tf-idf_{t,d} = tf_{t, d} \times idf_{t}
         """
)
"""
Intuitions on $tf-idf_{t,d}$:
* Highest when t occurs frequently in a small set of documents resulting in higher discriminating power
* Lower when term t occurs less frequently or occurs in multiple documents
* Lowest when term t occurs in almost all documents

A preliminary way to score documents for a query q would be to use the tf-idf weights for each query term and sum them up. In other words, for a query q containing multiple terms, we will go over each document and compute the a score. We will rank order the documents based on this score.

$Score(q, d) = \Sigma_{t \in q} tf-idf_{t,d}$

Here are the $tf-idf_{t,d}$ scores for all terms in the selected document.
"""
tf_idf_scores = {}
for term in tfs:
    tf_idf_scores[term] = tfs[term] * idfs[term]

st.text(tf_idf_scores)

"""
## Sample query processing
Let's use the tf-idf scoring to score document relevance. Say, we have two queries:
* Q1: experimental investigation
* Q2: slipstream investigation
You may notice that the first query is quite generic and may refer to any experiment. However, the second query is specific to slipstream. An ideal scoring scheme should rank document 1 higher for Q1 compared to Q2.

$Score(q, d) = \Sigma_{t \in q} tf-idf_{t,d}$
"""
q1 = "experimental investigation"
q2 = "slipstream investigation"


def score_document_for_a_query(query_text):
    tokens = TextPreProcessor(query_text).get_tokens()
    score = 0
    for token in tokens:
        score += tfs[token] * idfs[token]

    return score


st.write(f"document 1 score for q1: {score_document_for_a_query(q1)}")
st.write(f"document 1 score for q2: {score_document_for_a_query(q2)}")
"""
Using these scores, we would rank document 1 higher for q2.
"""
