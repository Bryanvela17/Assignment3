# Search Engine
import re
# from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import time
'''
Engine will show the top 5 results (no ranking, because boolean) for each result.
Full results will be output into a text file.
'''


class SearchEngine:
    def __init__(self, s, regExp, invertedIndex: str): # indexOfIndex: str
        self._stemmer = s  # Stemmer to use
        self._reg = regExp  # Regular expression to use

        self._invertedIndexFile = invertedIndex  # The string that stores the path to the inverted index.
        #self._indexOfIndex = self.loadIndexOfIndex(indexOfIndex)

    # def loadIndexOfIndex(self, indexOfIndex: str):
    #     '''
    #     Opens the index of index file specified by parameter, parses the
    #     file, returns a dictionary of the word and position, and closes file.
    #     '''
    #     returnable = dict()
    #     with open(indexOfIndex, 'r') as f:
    #         for line in f:
    #             entry = line.splitlines()
    #             returnable[entry[0]] = entry[1]
    #
    #     return returnable

    # def getUrls(self, query: str):
    #     '''
    #     Main functionality of the engine. Takes a query as a parameter and returns
    #     a list of all URLs that are relevant to that query.
    #     '''
    #
    #     # Parsing search query, getting the terms as stems
    #     # Tokens contains a dictionary of the token itself as the key and the position as the value
    #     tokens = self.parseSearch(query)
    #
    #     # Getting all token positions in the inverted index from the index of inverted index
    #     indexPositions = self.getIndexPositions(tokens)

    # def getIndexPositions(self, tokens: list):
    #     '''
    #     Takes a list of tokens as input. Returns a dictionary with the token as key
    #     and the seek() position as the value.
    #     '''
    #     positions = dict()
    #     for token in tokens:
    #         positions[token] = self._indexOfIndex[token]
    #
    #     return positions

    def parseSearch(self, query: str):
        '''
        Tokenizes + stems the search query and returns a dictionary of the words
        as the keys and its positions in the query as the value. Boolean retrieval model
        only uses the keys, while a phrase query will use the values for positions.
        '''
        returnable = dict()
        position = 0

        for token in re.findall(self._reg, query):
            token = self._stemmer.stem(token)
            if token not in returnable:
                returnable[token] = [position]
            else:
                returnable[token].append(position)

            position += 1

        return returnable


    def merge(self, parsedQuery, invertedIndexFile, mapping):
        with open(invertedIndexFile, 'r') as inverted_file, open(mapping, 'r') as mapping_file:
            inverted_contents = inverted_file.read()
            mapping_contents = mapping_file.read()

        queryDict = {}
        PostIDs_In_Common = []
        for word in parsedQuery:
            lines = inverted_contents.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith(word + ',') or line == word or line.endswith(',' + word):
                    queryDict[word] = line
        PostIDs_In_Common = find_common_documents(queryDict)
        return PostIDs_In_Common


def find_common_documents(queryDict):
    common_documents = set()

    # Get the lines from queryDict values
    lines = [value.split(',') for value in queryDict.values()]

    smallest_occurrences = []
    smallest_count = float('inf')

    # Find the smallest number of occurrences for the token
    for line in lines:
        count = int(line[1])
        if count < smallest_count:
            smallest_count = count
            smallest_occurrences = line[2:]

    # Iterate over the smallest number of occurrences
    for occurrence in smallest_occurrences:
        url_id, frequency = occurrence.split(':')
        x = url_id
        x_found = True
        # Check if x exists in all other lines
        for line in lines:
            if line[2:] != smallest_occurrences and not any(x in entry.split(':')[0] for entry in line[2:]):
                x_found = False
                break
        if x_found:
            common_documents.add(x)

    return common_documents



def get_urls_from_mapping(mapping_file, url_ids, limit=5):
    url_mapping = {}
    for line in mapping_file:
        url_id, url = line.strip().split(' ')
        url_mapping[url_id] = url

    urls = [url_mapping[url_id] for url_id in url_ids if url_id in url_mapping]
    return urls[:limit]

if __name__ == '__main__':
    invertedIndexFile = '/Users/bryanvela/Documents/CS121_Spring 2023_Information Retrieval/A3Milestone2/results.txt'
    mapping = '/Users/bryanvela/Documents/CS121_Spring 2023_Information Retrieval/A3Milestone2/mappings.txt'
    # CAUTION - This line of code takes a while! Make sure to only perform this initialization ONCE
    engine = SearchEngine(PorterStemmer(), re.compile('[a-zA-Z0-9]+'), invertedIndexFile )

    query = input("Please enter your query: ")
    print("You asked for: ", query)
    start_time = time.perf_counter()
    parsedQuery = engine.parseSearch(query)

    mergedPosting = engine.merge(parsedQuery, invertedIndexFile, mapping)
    with open(mapping, 'r') as mapping_file:
        urls = get_urls_from_mapping(mapping_file, mergedPosting, limit=5)
        print("Matching URLs (Top 5):")
        for url in urls:
            print(url)
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # Convert the execution time to minutes, seconds, and milliseconds
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    milliseconds = int((execution_time - int(execution_time)) * 1000)

    # Display the execution time
    print(f"Execution time: {minutes} minutes {seconds} seconds {milliseconds} milliseconds")
    print(len(mergedPosting))
