from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import os
import re

ALPHANUMERIC_WORDS = re.compile('[a-zA-Z0-9]+')

class Posting:
    def __init__(self, id, frequency):
        self._id = id
        self._frequency = frequency
        self._skipPtr = -1

    @property
    def id(self):
        return self._id
    
    @property
    def frequency(self):
        return self._frequency
    

    @property
    def skipPtr(self):
        return self._skipPtr

    def setSkipPtr(self, docId):
        self._skipPtr = docId
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

#assigns the skips to all the token's doc id:
#each doc id will be able to point to the 4th doc id
def assignSkips(index):
    for key, postings_list in index.items():
        listLength = len(postings_list) - 1
        for value in range(len(postings_list)):
            if value + 3 <= listLength:
                postings_list[value].setSkipPtr(postings_list[value + 3].id)
                #print(str(postings_list[value].skipPtr))

    # for token, postings_list in index.items():
    #     doc_ids = [str(posting.id) + ":" + str(posting.skipPtr) for posting in postings_list]
    #     print(token + ": " + ", ".join(doc_ids))

    return index
            


def find_dev_folder():
    # Function to find the "DEV" folder in the computer
    for root, dirs, files in os.walk('/', topdown=True):
        # if 'DEV' in dirs:
        #     return os.path.join(root, 'DEV')
        if 'testerFile' in dirs:
            return os.path.join(root, 'testerFile')
    return None




def run():
    # Data structure (dictionary) to hold the inverted index in memory
    index = dict()

    # Dictionary to hold the mapping between page ID and URL
    pageIDs = dict()

    pageCounter = 0
    urlCounter = 0  # Counter to keep track of the number of URLs parsed

    # Find the "DEV" folder in the computer
    dev_folder = find_dev_folder()
    if dev_folder is None:
        print("DEV folder not found.")
        return


    for folder in os.listdir(dev_folder):
        try:
            # Iterating through all the JSON files in the inner folder
            json_files = []
            folder_path = os.path.join(dev_folder, folder)

            if not os.path.isdir(folder_path):
                continue  # Skip non-directory entries

            for filename in os.listdir(folder_path):
                json_files.append(os.path.join(folder_path, filename))

            for json_file in json_files:
                try:
                    # Processing each JSON file
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

                    # Increment the URL counter and print the current count
                    urlCounter += 1
                    print(f"URLs parsed: {urlCounter}")
                except Exception as e:
                    print(f"Error parsing file {json_file}: {e}")
                    continue  # Skip to the next iteration

        except NotADirectoryError:
            print(f"{folder} is not a directory. Skipping.")
            continue  # Skip to the next iteration
    index = assignSkips(index)

    for token, postings_list in index.items():
        doc_ids = [str(posting.id) + ":" + str(posting.skipPtr) for posting in postings_list]
        print(token + ": " + ", ".join(doc_ids))

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


            
if __name__ == '__main__':
    run()