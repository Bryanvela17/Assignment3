# Test script to calculate the TF-IDF score of an example document
import math

def run():
    print(calculateTokenScore(23523, 55392, 1))

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

def testSeek():
    '''
    Function to test the seek() operation
    '''

    # Example query: pizza

    # Loading the indexOfIndex into memory
    indexOfIndex = dict()
    with open('indexOfIndex.txt', 'r') as f:
        for line in f:
            line = line.split()
            indexOfIndex[line[0]] = line[1]

    # Getting the byte position for pizza
    seekOffset1 = int(indexOfIndex['pizza'])
    seekOffset2 = int(indexOfIndex['chicken'])

    print(f"Seek Offset 1 Bytes: {seekOffset1}")
    print(f"Seek Offset 2 Bytes: {seekOffset2}")

    # Getting the posting list
    with open('results.txt', 'r') as f:
        f.seek(seekOffset1)
        postingList = f.readline()
        print(postingList)

        f.seek(seekOffset2)
        postingList = f.readline()
        print(postingList)

def testCosineSimilarity(queryFrequency: dict, documentFrequency: dict, idfScores: dict):
    '''
    Calculates the cosine similarity between a query and a document. Returns cosine similarity
    score.

    Components Needed:
    - Query - 
    - Term Frequency of the query itself
    - The IDF of each term from the inverted index

    - Document - 
    - Term Frequency of the words in the document

    @params
    queryFrequency - Dictionary of terms as keys and their frequencies as values. 
    documentFrequency - Dictionary of terms as keys and their frequencies as values.
    idfScores - Dictionary of terms as keys and their IDF scores as values.
    '''

    # Two dictionaries - one for query and one for document - to get weighted scores for cosine sim
    normalizedQuery = dict()
    normalizedDocument = dict()

    # Getting weighted term frequency (tf-wt)
    cosineScore = 0
    weightedSum = 0
    for term, frequency in queryFrequency.items():
        tfwt = 1 + math.log10(frequency)

        # Multiplying by idf to get wt
        wt = tfwt * idfScores[term]
        
        normalizedQuery[term] = wt

        # Now, normalizing wt by squaring the wt and adding it to a total. This total is sqrt'd and then divided each, stored into dict
        weightedSum += wt * wt

    # Taking sqrt of sum
    weightedSum = math.sqrt(weightedSum)

    # Dividing every wt by weighted sum
    for term, wt in normalizedQuery.items():
        normalizedQuery[term] = wt/weightedSum

    # Doing the same for documents
    # Getting weighted term frequency (tf-wt)
    weightedSumDocs = 0
    for term, frequency in documentFrequency.items():
        tfwt = 1 + math.log10(frequency)

        normalizedDocument[term] = tfwt

        # Don't need to multiply by idf
        # Getting normalized weight
        weightedSumDocs += tfwt * tfwt

    # Taking sqrt of sum
    weightedSumDocs = math.sqrt(weightedSumDocs)

    # Dividing every wt by weighted sum
    for term, wt in normalizedDocument.items():
        normalizedDocument[term] = wt/weightedSumDocs

        # Getting cosines
        if term in normalizedQuery:
            cosineScore += normalizedDocument[term] * normalizedQuery[term]

    return round(cosineScore, 5)


if __name__ == '__main__':
    #run()
    #testSeek()
    x = dict()
    x["best"] = 1
    x["car"] = 1
    x["insurance"] = 1

    y = dict()
    y["auto"] = 1
    y["car"] = 1
    y["insurance"] = 2

    idf = dict()
    idf["best"] = 1.3
    idf["car"] = 2.0
    idf["insurance"] = 3.0
    idf["auto"] = 2.3
    print(testCosineSimilarity(x, y, idf))