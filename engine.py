# Search Engine
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from invertedIndexCreatorBasic import Posting
import math


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

        self._urlMappings = self.loadUrlMappings() # Loads the url mappings file into a dictionary
        self._indexOfIndex = self.loadIndexOfIndex(indexOfIndex)

    def loadUrlMappings(self):
        mappings = dict()
        for line in self._urlMappingsFile:
            id, url = line.split()
            mappings[id] = url

        return mappings

    def loadIndexOfIndex(self, indexOfIndex: str):
        '''
        Opens the index of index file specified by parameter, parses the 
        file, returns a dictionary of the word and position, and closes file.
        '''
        returnable = dict()
        with open(indexOfIndex, 'r') as f:
            for line in f:
                entry = line.split()
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

        # Dictionary to hold IDF information
        termIDFs = dict()

        # Dictionary to hold postings information
        postings = dict()
        
        # Getting the appropriate information from the inverted index by seeking() to the correct position.
        for token in tokens:
            self._invertedIndexFile.seek(self._indexOfIndex[token])

            # Getting line
            information = self._invertedIndexFile.readline().split(',').strip()

            # Getting individual information
            idfScore = information[1]
            documentFrequency = information[2]
            postingList = information[3:]

            # Populating the two dictionaries
            termIDFs[token] = idfScore
            
            # Call Bryan's function on getting the intersection between the posting lists here. Get a dictionary where the term
            # is the key, and the value is a Posting object with the document ID and the term frequency or that term. 

        # Call cosine similarity function here. You loop through all the documents you found through the intersection.


        # Call term position function here


        # Call important terms here


        # Rank using a heap and return

        
    def _getNormalizedQueryValue(self, tokens: dict, idfScores: dict):
        '''
        Takes a dict of tokens and idfscore dictionary as input. Returns the normalized
        weighting of the query. 
        ''' 
        normalizedSum = 0
        tokenWeights = dict()
        for token, frequency in tokens.items():
            tfwt = 1 + math.log10(frequency)

            weight = tfwt * idfScores[token]
            tokenWeights[token] = weight

            normalizedSum += weight * weight

        normalizedSum = math.sqrt(normalizedSum) 

        for token, weight in tokenWeights.items():
            tokenWeights[token] = weight/normalizedSum

        return tokenWeights

      



    def merge(self, parsedQuery):
        '''
        Function that gets the posting lists of all the tokens in parsedQuery dictionary.
        Returns a list of all of the document Postings that have all words. 
        '''
        

    def getUrlMappings(self, documentIDs):
        returnable = []
        for documentID in documentIDs:
            returnable.append(self._urlMappings[documentID])

        return returnable

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
    # Open the mappings file, opening the index, parse into a dictionary, and put it into searchengine object
    with open('mappings.txt', 'r') as mappingsFile, open('results.txt', 'r') as invIndexFile:
        # CAUTION - This line of code takes a while! Make sure to only perform this initialization ONCE
        engine = SearchEngine(PorterStemmer(), re.compile('[a-zA-Z0-9]+'), invIndexFile, mappingsFile, 'indexOfIndex.txt')

        while True:
            # Prompt user for input - user can exit with ctrl C
            userQuery = input(">>> ")
            print(engine.getUrls(userQuery))


            

run()
