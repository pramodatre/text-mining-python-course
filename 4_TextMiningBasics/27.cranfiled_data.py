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
            print(self.cur_tag, self.prev_tag)
            self.prev_tag = self.cur_tag

        # Document doc = docs[0]
        doc_id = 10
        docs[doc_id].id = docs[doc_id].id.replace("\n", "").replace("\r", "")
        docs[doc_id].title = docs[doc_id].title.replace("\n", " ").replace("\r", "")
        docs[doc_id].author = docs[doc_id].author.replace("\n", " ").replace("\r", "")
        docs[doc_id].publication = (
            docs[doc_id].publication.replace("\n", " ").replace("\r", "")
        )
        docs[doc_id].abstract = (
            docs[doc_id].abstract.replace("\n", " ").replace("\r", "")
        )
        print(docs[doc_id])


@dataclass
class Document:
    id: str = ""
    title: str = ""
    author: str = ""
    publication: str = ""
    abstract: str = ""


class Query:
    pass


class RelevantDocs:
    pass


if __name__ == "__main__":
    cran_docs = Documents("/Users/anp2pi/Downloads/cran/cran.all.1400")
