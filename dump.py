from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
from urllib.parse import urldefrag
import os
import math
import re
import sys

ALPHANUMERIC_WORDS = re.compile('[a-zA-Z0-9]+')

class Posting:
    def __init__(self, id, frequency):
        self._id = id
        self._frequency = frequency


    @property
    def id(self):
        return self._id
    
    @property
    def frequency(self):
        return self._frequency
    
    def printPosting(posting):
        with open('postingOutput.txt', 'w') as file:
            file.write(f"Doc ID: {posting.id}\n")
            file.write(f"Frequency: {posting.frequency}\n")



'''
Code to parse JSON file and tokenize words alphanumerically, ignoring stopwords. Will also fix broken HTML
'''
def parseFile(filePath: str):
    
    # filePath is a path to a JSON object file. Get the URL and content from obj file.
    with open(filePath, 'r') as file:
        json_obj = json.load(file)

        url = json_obj['url']

        # Defragging the URL
        url, fragment = urldefrag(url)

        # Using beautifulsoup to parse HTML content
        page_obj = BeautifulSoup(json_obj['content'], 'lxml')

        # Tokenizing the text and storing in dictionary. Key (token) value (frequency)
        return (pageTokenize(page_obj), url)

def pageTokenize(page: object):
    '''
    Tokenizes the content retrieved from BeautifulSoup's get_text().
    Returns a dictionary of the tokens as keys and frequency as values. 
    This tokenizer also takes the *stems* from every token and stores it as
    keys. 
    '''

    # Tokenizing the page and storing tokens in a list
    #regTokenizer = RegexpTokenizer(r'\w+')
    #tokens = regTokenizer.tokenize(page.get_text())

    text = page.get_text()

    # Stemming each token and adding to a dictionary
    stemmer = PorterStemmer()
    stems = dict()
    for token in re.findall(ALPHANUMERIC_WORDS, text):
        stemmedWord = stemmer.stem(token)

        # Checking if it's already in the dictioanry - if it is, add by 1. If not, add a new entry
        if stemmedWord in stems:
            stems[stemmedWord] += 1
        else:
            stems[stemmedWord] = 1

    return stems

def calculateTokenScore(frequency, numDocumentsCorpus, numDocumentsTerm):
    '''
    Calculates the TF-IDF score for a single token and the amount of times this word appears in some document.
    Returns the TF-IDF score of the combination of these two.

    @params - frequency: int, numDocumentsCorpus: int, numDocumentsTerm: int
    @returns - score: float
    '''
    
    # First, calculating the weighting of the frequency
    tf = 0

    if frequency > 0:
        tf = 1 + math.log10(frequency)
    
    # Calculate the idf
    idf = math.log10(numDocumentsCorpus/numDocumentsTerm)
    return tf * idf

# def dumpIndex(index, counter):
#     if counter == 1:
#         filename = 'firstDump.txt'
#     elif counter == 2:
#         filename = 'secondDump.txt'
#     elif counter == 3:
#         filename = 'thirdDump.txt'
#     else:
#         return  # Invalid counter value

#     with open(filename, 'w', encoding='utf-8') as file:
#         for word, postings in index.items():
#             file.write(f"{word},{len(postings)}")
#             for post in postings:
#                 score = calculateTokenScore(post.frequency, len(pageIDs), len(postings))
#                 file.write(f",{post.id}:{score}")
#             file.write("\n")

def mergeFiles(filePaths, outputFile):
    with open(outputFile, 'a') as opFile:
        for fPath in filePaths:
            with open(fPath, 'r') as inputFile:
                content = inputFile.read()
                opFile.write(content)


def createInvertedIndex():
    # Data structure (dictionary) to hold the inverted index in memory
    index = dict()
    
    # Dictionary to hold the mapping between page ID and url
    pageIDs = dict()

    pageCounter = 0

    dumpCounter = 1
    # Iterating through all the inner folders in DEV folder
    path_to_inner = '../Assignment3/DEV/'
    for folder in os.listdir(path_to_inner):
        
        # Iterating through all the JSON files in the inner folder
        json_files = []

        for filename in os.listdir(os.path.join(path_to_inner, folder)):
            json_files.append(os.path.join(path_to_inner, folder, filename))
            

        for json_file in json_files:
            # Processing each json file
            words, url = parseFile(json_file)
            
            for word, counter in words.items():
               
                # Creating a posting
                post = Posting(pageCounter, counter)

                # Assigning to dictionary
                if word in index:
                    index[word].append(post)
                else:
                    index[word] = []
                    index[word].append(post)

        

                #calculate the size of the current inverted index
                # indexSize = sys.getsizeof(index)
                # print(indexSize)
                #if indexSize >= 70 then dump
                #1,093,129/3 = 364,376.33333
                if len(index) >= 364376 and dumpCounter != 3:
                    if dumpCounter == 1:
                        print("first")
                        filename = 'firstDump.txt'
                    elif dumpCounter == 2:
                        print("second")
                        filename = 'secondDump.txt'

                    #get the score of the current partial index and put it into the correct dump txt
                    with open(filename, 'w', encoding='utf-8') as file:
                        for word, postings in index.items():
                            file.write(f"{word, len(postings)},") #token, numberOfDocuments, docID:frequency 
                            for post in postings:
                                file.write(f"{post.id}:{post.frequency},")
                            file.write("\n")
                    #dumpIndex(index, dumpCounter)
                    index = {}
                    dumpCounter+=1
                elif dumpCounter == 3: #if the dumpCounter is 3 just get the rest of the index and put it into the third txt
                    print("third")
                    filename = 'thirdDump.txt'
                    #get the score of the current partial index and put it into the correct dump txt
                    with open(filename, 'w', encoding='utf-8') as file:
                        print("hello")
                        for word, postings in index.items():
                            file.write(f"{word, len(postings)},") #token, numberOfDocuments, docID:frequency 
                            for post in postings:
                                file.write(f"{post.id}:{post.frequency},")
                            file.write("\n")
                    #dumpIndex(index, dumpCounter)
                    index = {}


            #if the remaining isnt >= 70 then just dump the rest into the third file
            # if index:
            #     with open(filename, 'w', encoding='utf-8') as file:
            #         for word, postings in index.items():
            #             file.write(f"{word, len(pageIDs)},") #token, docID:frequency 
            #             for post in postings:
            #                 file.write(f",{post.id}:{post.frequency}")
            #             file.write("\n")
            #     index = {}


            # After processing, store a mapping between the actual file and the id
            pageIDs[pageCounter] = url
            pageCounter += 1

            #merge the files 
            filePaths = {"firstDump.txt", "secondDump.txt", "thirdDump.txt"}
            outputFilePath = "merged.txt"

            mergeFiles(filePaths,outputFilePath)
            
    # # Once finished, put output to file
    # with open('results.txt', 'w', encoding='utf-8') as f:
    #     new_index = sorted(index.items())

    #     for key, value in new_index:
    #         f.write(f"{key},{len(value)}")
    #         for post in value:

    #             # Calculating the TF-IDF Score and replacing the word frequency. 
    #             score = calculateTokenScore(post.frequency, len(pageIDs), len(value))
            
    #             f.write(f",{post.id}:{score}")
    #         f.write("\n")

    # with open('mappings.txt', 'w', encoding='utf-8') as f:
    #     for key, value in pageIDs.items():
    #         f.write(f"{key} {value}\n")

            
if __name__ == '__main__':
    createInvertedIndex()