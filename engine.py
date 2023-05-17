# Search Engine
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer


'''
Engine will show the top 5 results (no ranking, because boolean) for each result.
Full results will be output into a text file. 
'''

class SearchEngine:
    def __init__(self, s, regExp, invertedIndex: str, indexOfIndex: str):
        self._stemmer = s   # Stemmer to use
        self._reg = regExp  # Regular expression to use

        self._invertedIndexFile = invertedIndex # The string that stores the path to the inverted index.
        self._indexOfIndex = self.loadIndexOfIndex(indexOfIndex)

    def loadIndexOfIndex(self, indexOfIndex: str):
        '''
        Opens the index of index file specified by parameter, parses the 
        file, returns a dictionary of the word and position, and closes file.
        '''
        returnable = dict()
        with open(indexOfIndex, 'r') as f:



    def getUrls(self, query: str)


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
    

def run():

    # CAUTION - This line of code takes a while! Make sure to only perform this initialization ONCE
    engine = SearchEngine(PorterStemmer(), re.compile('[a-zA-Z0-9]+'))

    print(engine.parseSearch("master of software engineering"))
    print(engine.parseSearch("master of master software engineering"))

run()
