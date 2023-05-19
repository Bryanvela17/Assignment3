# Search Engine
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from main import Posting


'''
Engine will show the top 5 results (no ranking, because boolean) for each result.
Full results will be output into a text file. 
'''

class SearchEngine:
    def __init__(self, s, regExp, invertedIndexFile, urlMappingsFile, indexOfIndex = None):
        self._stemmer = s   # Stemmer to use
        self._reg = regExp  # Regular expression to use

        self._invertedIndexFile = invertedIndexFile # The OPEN FILE DESCRIPTOR of the inverted index.
        self._urlMappingsFile = urlMappingsFile # The OPEN FILE DESCRIPTOR of the mapping file.

        self._invertedIndex = self.testLoadInvertedIndex() # Test function - loads the entire inverted index into this dictionary
        self._urlMappings = self.loadUrlMappings() # Loads the url mappings file into a dictionary
        #self._indexOfIndex = self.loadIndexOfIndex(indexOfIndex)

    def loadUrlMappings(self):
        mappings = dict()
        for line in self._urlMappingsFile:
            id, url = line.split()
            mappings[id] = url

        return mappings

    def testLoadInvertedIndex(self):
        returnable = dict()
        for line in self._invertedIndexFile:
            parsed = line.split(',')
            token = parsed[0]
            numDocuments = parsed[1]
            postings = parsed[2:]

            returnable[token] = []

            for posting in postings:

                # Reconstructing the Posting object
                docID, frequency = posting.split(':')

                returnable[token].append(Posting(docID, frequency))
        
        return returnable

    def loadIndexOfIndex(self, indexOfIndex: str):
        '''
        Opens the index of index file specified by parameter, parses the 
        file, returns a dictionary of the word and position, and closes file.
        '''
        returnable = dict()
        with open(indexOfIndex, 'r') as f:
            for line in f:
                entry = line.splitlines()
                returnable[entry[0]] = entry[1]

        return returnable


    def getUrls(self, query: str):
        '''
        Main functionality of the engine. Takes a query as a parameter and returns
        a list of all URLs that are relevant to that query. 
        '''

        # Parsing search query, getting the terms as stems
        # Tokens contains a dictionary of the token itself as the key and the position as the value
        tokens = self.parseSearch(query)
        
        # List of Posting objects for every token.
        documentPostings = []

        for token in tokens:

            # Looking for matches in the inverted index
            documentPostings.append(self._invertedIndex[token])

        # Getting intersection
        if documentPostings:
            pass
            # Getting the intersection of all Document IDs 


            #result = set.intersection(*documentPostings, key=lambda Posting : Posting.id)
            
            # Getting the URLs. Returning the list of URLs.
            #return(self.getUrlMappings(result))
        
        '''
        # Getting all token positions in the inverted index from the index of inverted index
        indexPositions = self.getIndexPositions(tokens)

        # BOOLEAN RETRIEVAL MODEL
        # Now, merge all the postings together by getting the intersection - start with the list
        # with the smallest number of documents first, then go from there.
        # Getting postings
        postings = dict()
        

        
        for token, position in indexPositions.items():
            self._invertedIndex.seek(position)
            postings[token] = self.parsePosting(self._invertedIndex.readline())
        '''

    def getUrlMappings(self, documentIDs):
        returnable = []
        for documentID in documentIDs:
            returnable.append(self._urlMappings[documentID])

        return returnable

    # Experimental function
    #def getTopFive(self, documentIDs, )

    def parsePosting(self, line):

        return None

    def getIndexPositions(self, tokens: list):
        '''
        Takes a list of tokens as input. Returns a dictionary with the token as key
        and the seek() position as the value. 
        '''
        positions = dict()
        for token in tokens:
            positions[token] = self._indexOfIndex[token]

        return positions



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
    # Open the mappings file
    with open('mappings.txt', 'r') as mappingsFile:

        # Opening the index, parse into a dictionary, and put it into searchengine object
        with open('results.txt', 'r') as invIndexFile:
            # CAUTION - This line of code takes a while! Make sure to only perform this initialization ONCE
            engine = SearchEngine(PorterStemmer(), re.compile('[a-zA-Z0-9]+'), invIndexFile, mappingsFile)

            while True:
                # Prompt user for input - user can exit with ctrl C
                userQuery = input(">>> ")
                print(engine.getUrls(userQuery))


            

run()
