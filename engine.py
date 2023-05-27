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




    def merge(self, parsedQuery, invertedIndexFile, indexOfTheIndex, mapping):
        list = []
        with open(invertedIndexFile, "r") as file:
            for word in parsedQuery:
                position = indexOfTheIndex[word]
                file.seek(position)
                line = file.readline().strip()
                list.append(line)


        result = intersect(list)
        first_values = []
        for item in result:
            value = item.split(':')[0]
            first_values.append(value)
        displayValues(first_values, mapping)
        # return first_values


def displayValues(postIDS, mapping):
    count = 0  # Counter variable to track the number of values printed
    for item in postIDS:
        y = int(item)
        print(mapping[y])
        count += 1
        if count == 5:
            break
    print(len(postIDS))

def hasSkip(vector, index):
    try:
        hasSkip = int(vector[index].split(":")[2])
        return True
    except Exception:
        return False

def skip(vector, index) -> int:
    hasSkip = int(vector[index].split(":")[2])
    return hasSkip

def skipIndex(vector, index) -> int:
    findIndexOfSkip = int(vector[index].split(":")[3])
    return findIndexOfSkip

def intersect(lists):
    if len(lists) < 2:
        elements = lists[0].split(',')[2:]
        return [element.split(':')[0] for element in elements]

    # Sort the lists based on the first index in ascending order
    sorted_lists = sorted(lists, key=lambda x: int(x.split(",")[1]))

    answer_length = int(sorted_lists[0].split(",")[1].strip())
    # Initialize the intersection with the first sorted list
    answer = sorted_lists[0].split(",")[2:]  # Split the first sorted list and exclude the first two elements

    for i in range(1, len(sorted_lists)):

        current_list_length = int(sorted_lists[i].split(",")[1].strip())
        current_list = sorted_lists[i].split(",")[2:]  # Split the current sorted list and exclude the first two elements

        intersection = []  # Temporary list to store the intersection of the current list with the answer list

        p1 = 0  # Index for answer list
        p2 = 0  # Index for current list

        while p1 < answer_length and p2 < current_list_length:
            doc_id_1 = int(answer[p1].split(":")[0])  # Extract docID from answer list
            doc_id_2 = int(current_list[p2].split(":")[0])  # Extract docID from current list

            if doc_id_1 == doc_id_2:
                intersection.append(doc_id_1)
                p1 += 1
                p2 += 1
            elif doc_id_1 < doc_id_2:
                if hasSkip(answer, p1) and (skip(answer, p1) <= doc_id_2):
                    while hasSkip(answer, p1) and (skip(answer, p1) <= doc_id_2):
                        p1 = skipIndex(answer, p1)
                else:
                    p1 += 1
            else:
                if hasSkip(current_list, p2) and (skip(current_list, p2) <= doc_id_1):
                    while hasSkip(current_list, p2) and (skip(current_list, p2) <= doc_id_1):
                        p2 = skipIndex(current_list, p2)
                else:
                    p2 += 1

        answer = ['placeholder', str(len(intersection))] + [f"{element}:0" for element in intersection]  # Update the answer list with the intersection  # Update the answer list with the intersection
        answer_length = int(answer[1])
        answer = answer[2:]
    return answer


def read_mappings(filename):
    mappings = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                key, value = line.split(' ', 1)
                mappings[int(key)] = value
    return mappings

def read_indexOfIndex(filename):
    mappings = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                key, value = line.split(' ', 1)
                mappings[key] = int(value)
    return mappings


if __name__ == '__main__':
    invertedIndexFile = 'skiplist.txt'      # Inverted index with skip jumps made in SkipPointer.py
    mapping = 'mappings.txt'                # Mapping of DocIDs and URLs
    indexOfIndex = 'indexOfIndex.txt'       # index of Index make in indexOfIndexMaker.py
    mappings_dict = read_mappings(mapping)  # Mapping dict now im memory
    indexOfIndex_dict = read_indexOfIndex(indexOfIndex) # Inverted Index now in memory


    # CAUTION - This line of code takes a while! Make sure to only perform this initialization ONCE
    engine = SearchEngine(PorterStemmer(), re.compile('[a-zA-Z0-9]+'), invertedIndexFile )

    while True:
        query = input("Please enter your query: ")  # Asks the user for their query
        start_time = time.perf_counter()            # Timer begins counting the time
        parsedQuery = engine.parseSearch(query)     # Query is tokenized and parsed


        # Merge finds the intersection of the query using skip pointers and Index_of_Index,
        # the Inverted_Index, and the Mapping (Main works is done here)
        engine.merge(parsedQuery, invertedIndexFile, indexOfIndex_dict, mappings_dict)


        end_time = time.perf_counter()              # End the timer
        execution_time = end_time - start_time

        # Convert the execution time to minutes, seconds, and milliseconds
        minutes = int(execution_time // 60)
        seconds = int(execution_time % 60)
        milliseconds = int((execution_time - int(execution_time)) * 1000)

        # Display the execution time
        print(f"Execution time: {minutes} minutes {seconds} seconds {milliseconds} milliseconds")

