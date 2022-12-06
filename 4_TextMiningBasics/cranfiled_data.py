from dataclasses import dataclass


class Documents:
    def __init__(self, path_to_cranfield_documents_file: str) -> None:
        self.cur_tag = None
        self.prev_tag = None
        print(f"Reading contents form file {path_to_cranfield_documents_file}...")
        file = open(path_to_cranfield_documents_file, "r")
        lines = file.readlines()
        docs = []
        for line in lines:
            line = line.replace("\n", "").replace("\r", "")
            if line.startswith(".I"):
                self.cur_tag = "INDEX"
                if self.prev_tag == "ABSTRACT":
                    docs.append(cran_doc)
                cran_doc = Document()
                cran_doc.id = line.split(" ")[1]
            elif line.startswith(".T"):
                self.cur_tag = "TITLE"
            elif line.startswith(".A"):
                self.cur_tag = "AUTHOR"
            elif line.startswith(".B"):
                self.cur_tag = "PUBLICATION"
            elif line.startswith(".W"):
                self.cur_tag = "ABSTRACT"
            else:
                if self.cur_tag == "TITLE":
                    cran_doc.title += line
                elif self.cur_tag == "PUBLICATION":
                    cran_doc.publication += line
                elif self.cur_tag == "AUTHOR":
                    cran_doc.author += line
                elif self.cur_tag == "ABSTRACT":
                    cran_doc.abstract += line
            self.prev_tag = self.cur_tag

        self.docs = docs

    def get_all_docs(self):
        return self.docs


@dataclass
class Document:
    id: str = ""
    title: str = ""
    author: str = ""
    publication: str = ""
    abstract: str = ""


class Queries:
    def __init__(self, path_to_cranfield_query_file) -> None:
        self.cur_tag = None
        self.prev_tag = None
        print(f"Reading contents form file {path_to_cranfield_query_file}...")
        file = open(path_to_cranfield_query_file, "r")
        lines = file.readlines()
        queries = []
        query_index = 1
        for line in lines:
            line = line.replace("\n", "").replace("\r", "")
            if line.startswith(".I"):
                self.cur_tag = "INDEX"
                if self.prev_tag == "QUERY":
                    queries.append(query)
                query = Query()
                query.id = line.split(" ")[1]
                query.int_id = int(query.id)
                query_index += 1
            elif line.startswith(".W"):
                self.cur_tag = "QUERY"
            else:
                if self.cur_tag == "QUERY":
                    query.query_text += line
            self.prev_tag = self.cur_tag

        self.queries = queries

    def get_all_queries(self):
        return self.queries


@dataclass
class Query:
    id: str = None
    int_id: int = -1
    query_text: str = ""


class QueryReleventDocs:
    def __init__(self, path_to_cranqrel_file) -> None:
        print(f"Reading contents form file {path_to_cranqrel_file}...")
        file = open(path_to_cranqrel_file, "r")
        lines = file.readlines()
        query_id_relevant_docs = {}
        for line in lines:
            tokens = line.split(" ")
            if tokens[0] in query_id_relevant_docs:
                query_id_relevant_docs[tokens[0]].append(
                    {tokens[1]: tokens[2].replace("\n", "").replace("\r", "")}
                )
            else:
                query_id_relevant_docs[tokens[0]] = []
        self.query_id_relevant_docs = query_id_relevant_docs

    def get_query_relevantdocs_map(self):
        return self.query_id_relevant_docs


if __name__ == "__main__":
    cran_docs = Documents("/Users/pramodanantharam/Downloads/cran/cran.all.1400")
    cran_queries = Queries("/Users/pramodanantharam/Downloads/cran/cran.qry")
    cran_qrels = QueryReleventDocs(
        "/Users/pramodanantharam/Downloads/cran/cranqrel"
    ).get_query_relevantdocs_map()
    print(cran_qrels)
