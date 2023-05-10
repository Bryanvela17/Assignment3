from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup

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
        print(pageTokenize(page_obj))

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
    parseFile("../developer/DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json")

if __name__ == '__main__':
    run()