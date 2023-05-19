from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import os
import re
import math
from urllib.parse import urldefrag
import time

ALPHANUMERIC_WORDS = re.compile('[a-zA-Z0-9]+')


class Posting:
    def __init__(self, id, frequency):
        self._id = id
        self._frequency = frequency
        self._term_document_frequency = 0
        self._tfidf = None

    @property
    def id(self):
        return self._id

    @property
    def frequency(self):
        return self._frequency

    @property
    def term_document_frequency(self):
        return self._term_document_frequency

    def increment_term_document_frequency(self):
        self._term_document_frequency += 1

    @property
    def tfidf(self):
        return self._tfidf

    @tfidf.setter
    def tfidf(self, value):
        self._tfidf = value


def calculate_tfidf(index, pageIDs, num_documents, document_frequency):
    N = num_documents
    for term, postings in index.items():
        for posting in postings:
            df = document_frequency[term]  # Document frequency (number of documents containing the term)
            value = pageIDs[posting.id]
            url, word_count = value
            termFrequencyOfDocumentWeight = posting.frequency / word_count
            inverseDocumentFrequencyWeight = math.log10((N / (df + 1)))
            tf_idfWeight = termFrequencyOfDocumentWeight * inverseDocumentFrequencyWeight
            posting.tfidf = round(tf_idfWeight, 4)


def parseFile(filePath: str):
    with open(filePath, 'r') as file:
        json_obj = json.load(file)
        url = json_obj['url']
        page_obj = BeautifulSoup(json_obj['content'], 'lxml')
        return pageTokenize(page_obj), url


def pageTokenize(page: BeautifulSoup):
    text = page.get_text()
    stemmer = PorterStemmer()
    stems = dict()

    for token in re.findall(ALPHANUMERIC_WORDS, text):
        stemmedWord = stemmer.stem(token)
        if stemmedWord in stems:
            stems[stemmedWord] += 1
        else:
            stems[stemmedWord] = 1
    return stems


def find_dev_folder():

    # root_dir = '/Users/bryanvela/DEV'
    # for root, dirs, files in os.walk(root_dir, topdown=True):
    #     if 'alderis_ics_uci_edu' in dirs:
    #         return os.path.join(root, 'alderis_ics_uci_edu')
    # return None
    for root, dirs, files in os.walk('/', topdown=True):
        if 'DEV' in dirs:
            return os.path.join(root, 'DEV')
    return None


def process_json_file(json_file, index, pageIDs, pageCounter, urlCounter, document_frequency):
    try:
        words, url = parseFile(json_file)
        word_count = 0  # Initialize the word counter
        for word, counter in words.items():
            word_count += 1  # Increment the word counter

            post = Posting(pageCounter, counter)
            if word not in index:
                document_frequency[word] = 0
            if word in index:
                index[word].append(post)
            else:
                index[word] = [post]
            document_frequency[word] += 1
            # Increment the term document frequency for each posting
            # for posting in index[word]:
            #     posting.increment_term_document_frequency()

        pageIDs[pageCounter] = (url, word_count)  # Store URL and word count as a tuple in pageIDs
        pageCounter += 1
        urlCounter += 1
        print(f"URLs parsed: {urlCounter}")
    except Exception as e:
        print(f"Error parsing file {json_file}: {e}")

    return pageCounter, urlCounter


def write_output_to_file(index, pageIDs, document_frequency):
    with open('BryanResults.txt', 'w', encoding='utf-8') as f:
        with open('BryanMapping.txt', 'w', encoding='utf-8') as f2:
            new_index = sorted(index.items())
            for key, value in new_index:
                f.write(f"{key},{document_frequency[key]},")
                f.write(",".join(f"{posting.id}:{posting.frequency}" for posting in value))
                f.write("\n")
            f.close()

            # Sort pageIDs dictionary by URLs in alphabetical order
            # sorted_pageIDs = sorted(pageIDs.items(), key=lambda x: x[1][0])

            # f2.write("\n\nID Mappings\n")
            for key, value in pageIDs.items():
                url, word_count = value
                url, fragment = urldefrag(url)
                f2.write(f"{key} {url}\n")



def run():
    index = dict()
    pageIDs = dict()
    pageCounter = 0
    urlCounter = 0
    document_frequency = {}
    dev_folder = find_dev_folder()
    if dev_folder is None:
        print("DEV folder not found.")
        return

    for folder in os.listdir(dev_folder):
        try:
            json_files = []
            folder_path = os.path.join(dev_folder, folder)

            if not os.path.isdir(folder_path):
                continue

            for filename in os.listdir(folder_path):
                json_files.append(os.path.join(folder_path, filename))

            for json_file in json_files:
                pageCounter, urlCounter = process_json_file(json_file, index, pageIDs, pageCounter, urlCounter, document_frequency)
            calculate_tfidf(index, pageIDs, len(pageIDs), document_frequency)
        except NotADirectoryError:
            print(f"{folder} is not a directory. Skipping.")
    write_output_to_file(index, pageIDs, document_frequency)


def singleDir():
    index = dict()
    pageIDs = dict()
    pageCounter = 0
    urlCounter = 0
    document_frequency = {}
    dev_folder = find_dev_folder()
    if dev_folder is None:
        print("DEV folder not found.")
        return

    json_files = []
    for folder in os.listdir(dev_folder):
        folder_path = os.path.join(dev_folder, folder)
        json_files.append(folder_path)

    for json_file in json_files:
        pageCounter, urlCounter = process_json_file(json_file, index, pageIDs, pageCounter, urlCounter, document_frequency)
    calculate_tfidf(index, pageIDs, len(pageIDs), document_frequency)
    write_output_to_file(index, pageIDs, document_frequency)

if __name__ == '__main__':
    start_time = time.time()
    run()
    end_time = time.time()
    # Calculate the execution time in seconds
    execution_time = end_time - start_time

    # Convert the execution time to minutes and seconds
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)

    # Display the execution time
    print(f"Execution time: {minutes} minutes {seconds} seconds")
    # singleDir()
