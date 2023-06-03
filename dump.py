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



def mergeFiles(file1, file2, outputFilePath):
    with open(file1, 'r') as firstFile, open(file2, 'r') as secondFile, open(outputFilePath, 'w+') as outputFile:
        line1 = firstFile.readline().strip()
        line2 = secondFile.readline().strip()

        while line1 and line2:
            tokens1 = line1.split(',')  # token,docFreq, docID:freq
            tokens2 = line2.split(',')

            if tokens1[0] == tokens2[0]:
                # Merge the lines with matching tokens
                # newDocFreq = int(tokens1[1]) + int(tokens2[1])
                # newDocFreq = str(newDocFreq)
                #outputFile.write(tokens1[0] + "," + newDocFreq + "," + ",".join(tokens1[2:]) + ",".join(tokens2[2:]) + '\n')
                outputFile.write(tokens1[0] + "," + tokens1[1] + "," + ",".join(tokens1[2:]) + "," + ",".join(tokens2[2:]) + '\n')
                line1 = firstFile.readline().strip()  # increment the pointer in file1 down
                line2 = secondFile.readline().strip()  # increment the pointer in file2 down
            elif tokens1[0] < tokens2[0]:  # tokens1 line is the smallest
                outputFile.write(line1 + '\n')
                line1 = firstFile.readline().strip()  # increment the pointer in file1 down
            else:  # tokens2 line is the smallest
                outputFile.write(line2 + '\n')
                line2 = secondFile.readline().strip()  # increment the pointer in file2 down

        # Write remaining lines from file1, if any
        while line1:
            outputFile.write(line1 + '\n')
            line1 = firstFile.readline().strip()

        # Write remaining lines from file2, if any
        while line2:
            outputFile.write(line2 + '\n')
            line2 = secondFile.readline().strip()





def idfToTxt(fileName, completeFile, totalDocs):
    with open(fileName, 'r') as inputFile, open(completeFile, 'w') as complete:
        for line in inputFile:
            tokens = line.strip().split(',')
            if len(tokens) >= 3:
                numberOfDocs = len(tokens) - 3 #gets how many posting objects there are 
                idf = math.log10(totalDocs / numberOfDocs)
                subArray = tokens[2:]
                subArray = [x for x in subArray if x]  # Filter out empty elements
                subArray = sorted(subArray, key=lambda x: int(x.split(':')[0]))
                sorted_line = tokens[0] + ',' + str(idf) + ',' + str(numberOfDocs) + ','
                sorted_line += ','.join(subArray)
                complete.write(sorted_line + '\n')
            else:
                # Write the original line to the output file
                complete.write(line)


def dump(index, dumpCounter):
    filename = ""
    if dumpCounter == 1:
        filename = "firstDump.txt"
    elif dumpCounter == 2:
        filename = "secondDump.txt"
    else:
        filename = "thirdDump.txt"
    sortedIndex = dict(sorted(index.items())) #sorts index by key so that the dumps will 0be sorted
    with open(filename, 'w', encoding='utf-8') as file:
        for word, postings in sortedIndex.items():
            file.write(f"{word.strip()},{len(postings)},")  # token, numberOfDocuments,
            for post in postings:
                file.write(f"{post.id}:{post.frequency},")
                #print(post.id)
            file.write("\n")
        
    
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
            if len(index) < 363644:
                words, url = parseFile(json_file)
                for word, counter in words.items():
                    post = Posting(pageCounter, counter)
                    if word in index:
                        index[word].append(post)
                    else:
                        index[word] = [post]
            pageIDs[pageCounter] = url
            pageCounter += 1

            if len(index) >= 363644 and dumpCounter <= 3:
                dump(index, dumpCounter)
                index = {}
                dumpCounter += 1    
            
        if(len(index) > 0):
            dump(index,4) #dump into leftover
 

    #merge first and second
    mergeFiles("firstDump.txt", "secondDump.txt", "merged.txt")
    #merge merged and third into finalMerged
    mergeFiles("thirdDump.txt", "fourthDump.txt", "secondMerged.txt")
    mergeFiles("merged.txt", "secondMerged.txt", "finalMerged.txt")
   # mergeFiles("thirdDump.txt", "merged.txt", "finalMerged.txt")
    idfToTxt("finalMerged.txt", "completeMerge.txt", len(pageIDs))

    
        
            
    
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