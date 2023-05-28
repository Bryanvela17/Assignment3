# Iterates through the inverted index and rewrites new entries, calculating the TF-IDF score in place of word frequencies
import math

def calculateScores(fileName, numDocuments):
    '''
    Takes a string as input. Opens the specified string and parses the entire inverted index,
    modifying the word frequency and converting it into document's respective TF-IDF score.
    This uses N as specified in the parameter and the document frequency as the second
    index in the posting list. 
    '''

    with open(fileName, 'r') as file:
        
        # Iterating through all the lines in the file, parsing each one
        # An example line parse looks like this: nynex,10,26657:2,28859:2,30754:1,33246:2,35875:1,39668:3,43445:1,44955:1,47952:1,49131:1
        for line in file:
            line = line.split(',')

            token = line[0]         # Token
            docFrequency = line[1]  # Document Frequency
            postingList = line[2:]  # Posting list



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

        




if __name__ == '__main__':
    calculateScores('results.txt', 55392)
