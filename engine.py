import re
from nltk.stem import PorterStemmer

class SearchEngine:
    def __init__(self, stemmer, regExp, invertedIndexFile, mappingFile):
        self._stemmer = stemmer
        self._reg = regExp
        self._invertedIndexFile = invertedIndexFile
        self._mappingFile = mappingFile

    def parseSearch(self, query):
        return [self._stemmer.stem(token) for token in re.findall(self._reg, query)]

    def retrieveDocuments(self, query):
        parsedQuery = self.parseSearch(query)
        documentSets = self.merge(parsedQuery)
        return self.getUrls(documentSets)

    def merge(self, parsedQuery):
        with open(self._invertedIndexFile, 'r') as inverted_file:
            inverted_contents = inverted_file.readlines()

        documentSets = []
        for term in parsedQuery:
            search_term = f"{term},"
            matches = [line.strip() for line in inverted_contents if line.startswith(search_term)]
            if matches:
                doc_ids = set()
                for match in matches:
                    doc_list = match.split(',')[2:]
                    doc_ids.update([doc_freq.split(':')[0] for doc_freq in doc_list])
                documentSets.append(doc_ids)

        # Perform boolean intersection of document sets
        if documentSets:
            result = set.intersection(*documentSets)
            return [result]
        else:
            return []

    def getUrls(self, documentSets):
        urls = set()  # Use a set to store unique URLs
        with open(self._mappingFile, 'r') as mapping_file:
            mapping_contents = mapping_file.readlines()

        intersected_docs = set.intersection(*documentSets)
        for line in mapping_contents:
            doc_id, url = line.strip().split()
            if doc_id in intersected_docs:
                urls.add(url)

        return urls


if __name__ == '__main__':
    invertedIndexFile = '/Users/brandonvela/ICS121_InfoRetrieval/Milestone1/results_3.txt'
    mappingFile = '/Users/brandonvela/ICS121_InfoRetrieval/Milestone1/mappings.txt'
    engine = SearchEngine(PorterStemmer(), re.compile('[a-zA-Z0-9]+'), invertedIndexFile, mappingFile)

    query = input("Please enter your query: ")
    documents = engine.retrieveDocuments(query)

    if len(documents) > 0:
        print("Relevant documents:")
        for doc in documents:
            print(doc)
    else:
        print("No relevant documents found.")
