import json                         # For json loading
import pprint                       # For pretty print
from bs4 import BeautifulSoup       # For parsing files
import re   # For regex
import os   # For traversing directories
from collections import defaultdict  # Manually Added
import hashlib                       # Manually Added

##################################################################################################################################################
from nltk.stem import PorterStemmer
##################################################################################################################################################

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#words_in_urls = defaultdict(list)   # Maps each token/word with the url it appears in
tokenFrequency = defaultdict(int)   # Maps each token/word with the respective frequency
urlFrequency = defaultdict(int)
ALPHANUMERIC_WORDS = re.compile('[a-zA-Z0-9]+')





##################################################################################################################################################
#andy's additions
stemmer = PorterStemmer()
words_in_urls = defaultdict(list)   # Maps each token/word with a Posting object that contains the urlID and the frequency 



#for postings
class Postings:
    def __init__(self, urlID = 0, frequency = 0):
        self.urlID
        self.frequency


#passes the token into the stem object and stems the word, then returns the stemmed word
def stemmer(token):
    stemmedWord = stemmer.stem(token)
    return stemmedWord

#pairs the url to the token in the dictionary
#assumes that the frequency and urlID is already calculated before putting it into the inverter
def invertedIndexer(token,urlID,frequency):
    newPosting = Postings(urlID,frequency)
    words_in_urls[token].append(newPosting)


##################################################################################################################################################





def create_url_hash(tokens, url):
    hash_object = hashlib.sha256(url.encode())
    hash_value = int(hash_object.hexdigest(), 16)  # convert hash value to integer
    for w in tokens:
        if w not in words_in_urls:
            words_in_urls[w] = [hash_value]
            urlFrequency[w] = 1  # Initialize URL frequency count to 1
        else:
            if hash_value not in words_in_urls[w]:
                words_in_urls[w].append(hash_value)
                urlFrequency[w] += 1  # Increment URL frequency count
    pprint.pprint(words_in_urls)
    pprint.pprint(urlFrequency)


def token_frequency(tokens):
    if tokens is not None:
        for word in tokens:
            if word not in tokenFrequency:
                tokenFrequency[word] = 1
            else:
                tokenFrequency[word] += 1


def get_tokens(soup, url_name) -> list:
    tokens = []
    all_text = soup.get_text()
    all_text = all_text.strip().split()
    for word in all_text:
        word = word.lower()
        alphanum_tokens = re.findall(ALPHANUMERIC_WORDS, word)
        for w in alphanum_tokens:
            if len(w) >= 2:
                tokens.append(w)
    create_url_hash(tokens, url_name)
    token_frequency(tokens)
    return tokens


def parse_single_file(filename):
    with open(filename) as f:
        data = json.load(f)
        soup = BeautifulSoup(data['content'], 'html.parser')
        url_name = data['url']
        print(f'This is the url name: {url_name}')
        tokens = get_tokens(soup, url_name)
        # print(f'------------------------------------')
        # print(f'Below is the list of tokens found in current url: ')
        # pprint.pprint(tokens)
        # print(f'------------------------------------')
        # print(f'Below is the list of tokens/frequency for all pages indexed: ')
        # pprint.pprint(tokenFrequency)


def parse_json_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                parse_single_file(filepath)

        # print(all_text)
        # data['content'] = soup.prettify()
        # pprint.pprint(data, width=200)  # Set width to 120 to avoid line truncation


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_json_files('/Users/bryanvela/Documents/ICS121_Spring 2023_Information Retrieval/Assignment-3/DEV/'
                     'aiclub_ics_uci_edu')
    # parse_single_file('/Users/bryanvela/Documents/ICS121_Spring 2023_Information Retrieval/Assignment-3/DEV/aiclub_i
    # cs_'
    #                   'uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json')