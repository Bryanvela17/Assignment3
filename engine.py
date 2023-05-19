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
        return self.getTopUrls(documentSets)

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

    def getTopUrls(self, documentSets):
        url_scores = {}
        with open(self._mappingFile, 'r') as mapping_file:
            mapping_contents = mapping_file.readlines()

        intersected_docs = set.intersection(*documentSets)
        for line in mapping_contents:
            doc_id, url = line.strip().split()
            if doc_id in intersected_docs:
                url_scores[url] = url_scores.get(url, 0) + 1

        # Sort URLs based on score (frequency of occurrence)
        sorted_urls = sorted(url_scores, key=url_scores.get, reverse=True)

        # Return top 5 URLs
        return sorted_urls[:5]


if __name__ == '__main__':
    invertedIndexFile = '/home/bovela/121M1/Assignment3/results_3.txt'
    mappingFile = '/home/bovela/121M1/Assignment3/mappings.txt'
    engine = SearchEngine(PorterStemmer(), re.compile('[a-zA-Z0-9]+'), invertedIndexFile, mappingFile)

    print("Enter a query or press Ctrl+C to exit.")
    try:
        while True:
            query = input("Please enter your query: ")
            top_urls = engine.retrieveDocuments(query)

            if len(top_urls) > 0:
                print("Top 5 relevant documents:")
                for url in top_urls:
                    print(url)
            else:
                print("No relevant documents found.")
    except KeyboardInterrupt:
        print("Exiting...")

