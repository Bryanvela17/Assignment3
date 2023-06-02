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

def mergeFiles(file1, file2, file3, outputFilePath, totalDocs):
    with open(file1, 'r') as firstFile, open(file2, 'r') as secondFile, open(file3, 'r') as thirdFile, open(outputFilePath, 'w+') as outputFile: #opens all txt at once
        line1 = firstFile.readline().strip()
        line2 = secondFile.readline().strip()
        line3 = thirdFile.readline().strip()

        while line1 and line2 and line3:
            tokens1 = line1.split(',') #token,docFreq, docID:freq
            tokens2 = line2.split(',') 
            tokens3 = line3.split(',')

            if tokens1[0] == tokens2[0] and tokens2[0] == tokens3[0]:
                # Merge the lines with matching tokens
                newDocFreq = int(tokens1[1]) + int(tokens2[1]) + int(tokens3[1])
                newDocFreq = str(newDocFreq)
                outputFile.write(tokens1[0] + "," + newDocFreq + "," + ",".join(tokens1[2:]) + ",".join(tokens2[2:]) + ",".join(tokens3[2:]) + '\n')
                line1 = firstFile.readline().strip()  # increment the pointer in file1 down
                line2 = secondFile.readline().strip()  # increment the pointer in file2 down
                line3 = thirdFile.readline().strip()  # increment the pointer in file3 down
            elif tokens1[0] < tokens2[0] and tokens1[0] < tokens3[0]:  # tokens1 line is the smallest
                outputFile.write(line1 + '\n')
                line1 = firstFile.readline().strip()  # increment the pointer in file1 down
            elif tokens2[0] < tokens1[0] and tokens2[0] < tokens3[0]:  # tokens2 line is the smallest
                outputFile.write(line2 + '\n')
                line2 = secondFile.readline().strip()  # increment the pointer in file2 down
            elif tokens3[0] < tokens1[0] and tokens3[0] < tokens2[0]:  # tokens3 line is the smallest
                outputFile.write(line3 + '\n')
                line3 = thirdFile.readline().strip()  # increment the pointer in file3 down
            elif tokens1[0] == tokens2[0] and tokens1 != tokens3[0]:
                # Merge lines from file1 and file2
                newDocFreq = int(tokens1[1]) + int(tokens2[1])
                newDocFreq = str(newDocFreq)
                outputFile.write(tokens1[0] + "," + newDocFreq + "," + ",".join(tokens1[2:]) + ",".join(tokens2[2:]) + '\n')
                line1 = firstFile.readline().strip()  # increment the pointer in file1 down
                line2 = secondFile.readline().strip()  # increment the pointer in file2 down
            elif tokens1[0] == tokens3[0] and tokens1[0] != tokens2[0]:
                # Merge lines from file1 and file3
                newDocFreq = int(tokens1[1]) + int(tokens3[1])
                newDocFreq = str(newDocFreq)
                outputFile.write(tokens1[0] + "," + newDocFreq + "," + ",".join(tokens1[2:]) + ",".join(tokens3[2:]) + '\n')
                line1 = firstFile.readline().strip()  # increment the pointer in file1 down
                line3 = thirdFile.readline().strip()  # increment the pointer in file3 down
            elif tokens2[0] == tokens3[0] and tokens2[0] != tokens1[0]:
                # Merge lines from file2 and file3
                newDocFreq = int(tokens2[1]) + int(tokens3[1])
                newDocFreq = str(newDocFreq)
                outputFile.write(tokens2[0] + "," + newDocFreq + "," + ",".join(tokens2[2:]) + ",".join(tokens3[2:]) + '\n')
                line2 = secondFile.readline().strip()  # increment the pointer in file2 down
                line3 = thirdFile.readline().strip()  # increment the pointer in file3 down

        if line1 == '' and line2 != '' and line3 != '': #merge for just file2 and 3 
            while line2 and line3:
                tokens2 = line2.split(',') 
                tokens3 = line3.split(',')
                if tokens2[0] < tokens3[0]:
                    outputFile.write(tokens2[0] + "," + tokens2[1] + ",".join(tokens2[2:]) + '\n')
                    line2 = secondFile.readline().strip()  # increment the pointer in file2 down
                elif tokens3[0] < tokens2[0]:
                    outputFile.write(tokens3[0] + "," + tokens3[1] + ",".join(tokens3[2:]))
                    line3 = thirdFile.readline().strip()  # increment the pointer in file2 down
                else: #2 and 3 are equal
                    newDocFreq = int(tokens2[1]) + int(tokens3[1]) 
                    newDocFreq = str(newDocFreq)
                    outputFile.write(tokens2[0] + "," + newDocFreq + "," + ",".join(tokens2[2:]) + ",".join(tokens3[2:]) + '\n')
                    line2 = secondFile.readline().strip()  # increment the pointer in file2 down
                    line3 = thirdFile.readline().strip()  # increment the pointer in file3 down
            if line2 == '' and line3 != '':
                while line3: #put the left over into the output file 
                    outputFile.write(line3 + '\n')
                    line3 = thirdFile.readline().strip()
        elif line2 == '' and line1 != '' and line3 != '':
            while line1 and line3:
                tokens1 = line1.split(',')
                tokens3 = line3.split(',')
                if tokens1[0] < tokens3[0]:
                    outputFile.write(tokens1[0] + "," + tokens1[1] + ",".join(tokens1[2:]) + '\n')
                    line1 = firstFile.readline().strip()  # increment the pointer in file1 down
                elif tokens3[0] < tokens1[0]:
                    outputFile.write(tokens3[0] + "," + tokens3[1] + ",".join(tokens3[2:]) + '\n')
                    line3 = thirdFile.readline().strip()  # increment the pointer in file3 down
                else:  # 1 and 3 are equal
                    newDocFreq = int(tokens1[1]) + int(tokens3[1])
                    newDocFreq = str(newDocFreq)
                    outputFile.write(tokens1[0] + "," + newDocFreq + "," + ",".join(tokens1[2:]) + ",".join(tokens3[2:]) + '\n')
                    line1 = firstFile.readline().strip()  # increment the pointer in file1 down
                    line3 = thirdFile.readline().strip()  # increment the pointer in file3 down
            if line1 == '' and line3 != '':
                while line3:  # put the left over into the output file
                    outputFile.write(line3 + '\n')
                    line3 = thirdFile.readline().strip()
        elif line3 == '' and line1 != '' and line2 != '':
            while line1 and line2:
                tokens1 = line1.split(',')
                tokens2 = line2.split(',')
                if tokens1[0] < tokens2[0]:
                    outputFile.write(tokens1[0] + ", " + tokens1[1] + ", ".join(tokens1[2:]) + '\n')
                    line1 = firstFile.readline().strip()  # increment the pointer in file1 down
                elif tokens2[0] < tokens1[0]:
                    outputFile.write(tokens2[0] + ", " + tokens2[1] + ", ".join(tokens2[2:]) + '\n')
                    line2 = secondFile.readline().strip()  # increment the pointer in file2 down
                else:  # 1 and 2 are equal
                    newDocFreq = int(tokens1[1]) + int(tokens2[1])
                    newDocFreq = str(newDocFreq)
                    outputFile.write(tokens1[0] + ", " + newDocFreq + ", " + ", ".join(tokens1[2:]) + ", ".join(tokens2[2:]) + '\n')
                    line1 = firstFile.readline().strip()  # increment the pointer in file1 down
                    line2 = secondFile.readline().strip()  # increment the pointer in file2 down
            if line1 == '' and line2 != '':
                while line2:  # put the left over into the output file
                    outputFile.write(line2 + '\n')
                    line2 = secondFile.readline().strip()
        elif line1 != '' and line2 == '' and line3 == '':
            while line1:  # put the left over into the output file
                outputFile.write(line1 + '\n')
                line1 = firstFile.readline().strip()
        elif line1 == '' and line2 != '' and line3 == '':
            while line2:  # put the left over into the output file
                outputFile.write(line2 + '\n')
                line2 = secondFile.readline().strip()
        elif line1 == '' and line2 == '' and line3 != '':
            while line3:  # put the left over into the output file
                outputFile.write(line3 + '\n')
                line3 = thirdFile.readline().strip()


        with open("merged.txt", 'r') as inputFile, open("finalMerged.txt", 'w') as sortedFile:
            for line in inputFile:
                tokens = line.strip().split(',')
                if len(tokens) >= 3:
                    numberOfDocs = int(tokens[1])
                    idf = math.log10(totalDocs/numberOfDocs)
                    subArray = tokens[2:]
                    subArray = [x for x in subArray if x]  # Filter out empty elements
                    subArray = sorted(subArray, key=lambda x: int(x.split(':')[0]))
                    sorted_line = tokens[0] + ',' + str(idf) + ',' + tokens[1] + ','
                    sorted_line += ','.join(subArray)
                    #sorted_line = ','.join(tokens[:2] + subArray)
                    sortedFile.write(sorted_line + '\n')
                else:
                    # Write the original line to the output file
                    sortedFile.write(line)

        print("total doc frq " + str(totalDocs))

        # outputFile.seek(0) #reset to the top of the output file
        # #sort all the posting lists from least to greatest 
        # for lines in outputFile:
        #     print("hello")
        #     # Split the line into tokens
        #     tokens = lines.strip().split(',')

        #     if len(tokens) >= 3:  # Check if there are enough elements in the token
        #         # Sort the tokens from index 2 onward based on the value after the second comma
        #         print(tokens)
        #         subArray = tokens[2:]
        #         subArray = [x for x in subArray if x]  # Filter out empty elements
        #         subArray = sorted(subArray, key=lambda x: int(x.split(':')[0]))
        #         sorted_line = ', '.join(tokens[:2] + subArray)

        #         # Write the sorted line to the output file
        #         outputFile.write(sorted_line + '\n')
        #     else:
        #         # Write the original line to the output file
        #         outputFile.write(lines)
            


   





    # with open(outputFilePath, "w+") as outputFile:
    #     for file in filePath:
    #         with open(file, "r") as inputFile:
    #             for line in inputFile:  # Goes line by line checking if the current token exists in the merged txt
    #                 tokens = line.strip().split()
    #                 tokenLineNumber = findTokenTXT(outputFile, tokens[0])
    #                 if tokenLineNumber != -1:  # If the token exists in merge, append the posting list to the corresponding token
    #                     lineCounter = 0
    #                     outputFile.seek(0)  # Move the file pointer back to the beginning of the file
    #                     for outputLine in outputFile:
    #                         if tokenLineNumber == lineCounter:  # On the correct line to append
    #                             outputLine = outputLine.rstrip()  # Remove trailing newline
    #                             outputToken = outputLine.strip().split()
    #                             totalDocFrequency = int(tokens[1]) + int(outputToken[1]) #change the total doc frequency for the line
    #                             totalDocFrequency = str(totalDocFrequency)
    #                             newOutputString = outputToken[0] + ',' + totalDocFrequency #token + docFreq
    #                             outputList = ",".join(tokens[2:])
    #                             newOutputString += outputList #puts the posting list to token,docFreq 
    #                             inputList = ",".join(tokens[2:])  # Get the posting list from the input
    #                             newOutputString = newOutputString + inputList
    #                             outputFile.write(newOutputString + "\n")  # Write the line to the output file
    #                         lineCounter += 1
    #                 else:
    #                     outputFile.write(line + "\n")

                


def findTokenTXT(file, token):
    with open(file, 'r') as f:
        lines = f.readlines()

    line_number = -1
    for i, line in enumerate(lines, start=1):
        if token in line:
            line_number = i
            break
    return line_number #if it returns -1 the token is not in the file





def dump(index, dumpCounter):
    filename = "firstDump.txt"
    if dumpCounter == 1:
        filename = "firstDump.txt"
    elif dumpCounter == 2:
        filename = "secondDump.txt"
    elif dumpCounter == 3:
        filename = "thirdDump.txt"
    sortedIndex = dict(sorted(index.items())) #sorts index by key so that the dumps will 0be sorted
    with open(filename, 'w', encoding='utf-8') as file:
        for word, postings in sortedIndex.items():
            file.write(f"{word},{len(postings)},")  # token, numberOfDocuments,
            for post in postings:
                file.write(f"{post.id}:{post.frequency},")
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
            # Processing each json file
            if len(index) < 364376:
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
                    
            #dump if over threshold
            else:
                #dump(index,dumpCounter)
                with open("output.txt", "w") as file:
                    for word, posting_list in index.items():
                        posting_strings = [str(posting) for posting in posting_list]
                        line = word + " " + " ".join(posting_strings)
                        file.write(line + "\n")
                index = {}
                dumpCounter +=1

        #calculate the size of the current inverted index
        # indexSize = sys.getsizeof(index)
        # print(indexSize)
        #if indexSize >= 70 then dump
        #1,093,129/3 = 364,376.33333
        # if len(index) >= 364376 and dumpCounter != 3:
        #     if dumpCounter == 1:
        #         print("first")
        #         filename = 'firstDump.txt'
        #     elif dumpCounter == 2:
        #         print("second")
        #         filename = 'secondDump.txt'

        #     #get the score of the current partial index and put it into the correct dump txt
        #     with open(filename, 'w', encoding='utf-8') as file:
        #         for word, postings in index.items():
        #             file.write(f"{word, len(postings)},") #token, numberOfDocuments, docID:frequency 
        #             for post in postings:
        #                 file.write(f"{post.id}:{post.frequency},")
        #             file.write("\n")
        #     #dumpIndex(index, dumpCounter)
        #     index = {}
        #     dumpCounter+=1
        # elif dumpCounter == 3: #if the dumpCounter is 3 just get the rest of the index and put it into the third txt
        #     print("third")
        #     filename = 'thirdDump.txt'
        #     #get the score of the current partial index and put it into the correct dump txt
        #     with open(filename, 'w', encoding='utf-8') as file:
        #         print("hello")
        #         for word, postings in index.items():
        #             file.write(f"{word, len(postings)},") #token, numberOfDocuments, docID:frequency 
        #             for post in postings:
        #                 file.write(f"{post.id}:{post.frequency},")
        #             file.write("\n")
        #     #dumpIndex(index, dumpCounter)
        #     index = {}


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
    


        
    #mergeFiles("firstDump.txt", "secondDump.txt", "thirdDump.txt", "merged.txt", len(pageIDs))
            
    if findTokenTXT("firstDump.txt", "for"):
        print("true")
    else:
        print("false")
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