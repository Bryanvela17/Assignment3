from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import os

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

'''
Code to parse JSON file and tokenize words alphanumerically, ignoring stopwords. Will also fix broken HTML
'''
def parseFile(filePath: str):
    
    # filePath is a path to a JSON object file. Get the URL and content from obj file.
    with open(filePath, 'r') as file:
        json_obj = json.load(file)

        url = json_obj['url']

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
    regTokenizer = RegexpTokenizer(r'\w+')
    tokens = regTokenizer.tokenize(page.get_text())

    # Stemming each token and adding to a dictionary
    stemmer = PorterStemmer()
    stems = dict()
    for token in tokens:
        stemmedWord = stemmer.stem(token)

        # Checking if it's already in the dictioanry - if it is, add by 1. If not, add a new entry
        if stemmedWord in stems:
            stems[stemmedWord] += 1
        else:
            stems[stemmedWord] = 1

    return stems


def run():
    # Data structure (dictionary) to hold the inverted index in memory
    index = dict()

    # Dictionary to hold the mapping between page ID and url
    pageIDs = dict()

    pageCounter = 0

    # Iterating through all the inner folders in DEV folder
    path_to_inner = '../developer/DEV/'
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

            # After processing, store a mapping between the actual file and the id
            pageIDs[pageCounter] = url
            pageCounter += 1

    # Once finished, put output to file
    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write(f"Number of indexed documents: {len(pageIDs)}\n")
        f.write(f"Number of tokens: {len(index)}\n")
        f.write(f"Inverted Index\n")

        for key, value in index.items():
            f.write("\n------------------------------------------------\n")
            f.write(f"Token: {key} - Documents: ")
            for post in value:
                f.write(f"{post.id}:{post.frequency} ")

        f.write(f"ID Mappings")
        for key, value in pageIDs.items():
            f.write(f"{key} {value}\n")



    #parseFile("../developer/DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json")

if __name__ == '__main__':
    run()