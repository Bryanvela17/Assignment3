import json                         # For json loading
# import pprint                       # For pretty print
from bs4 import BeautifulSoup       # For parsing files
import re   # For regex
import os   # For traversing directories
# from collections import default dict  # Manually Added
import hashlib                       # Manually Added
from Posting import Posting
from porter2stemmer import Porter2Stemmer

ALPHANUMERIC_WORDS = re.compile('[a-zA-Z0-9]+')
token_posting = {}
number_of_indexed_documents = 0


def create_url_hash(url):
    hash_object = hashlib.sha256(url.encode())
    hash_value = int(hash_object.hexdigest(), 16)  # convert hash value to integer
    return hash_value


def update_token_posting(token, url):
    if token in token_posting:
        token_posting[token].update_url_hash(url)
    else:
        post = Posting()
        post.update_url_hash(url)
        token_posting[token] = post


def get_tokens(soup, url_name) -> None:
    all_text = soup.get_text()
    all_text = all_text.strip().split()
    for word in all_text:
        word = word.lower()
        alphanum_tokens = re.findall(ALPHANUMERIC_WORDS, word)
        for w in alphanum_tokens:
            if len(w) >= 2:
                stemmer = Porter2Stemmer()
                update_token_posting(stemmer.stem(w), create_url_hash(url_name))


def parse_single_file(filename):
    with open(filename) as f:
        global number_of_indexed_documents
        number_of_indexed_documents += 1
        data = json.load(f)
        soup = BeautifulSoup(data['content'], 'html.parser')
        url_name = data['url']
        # print(f'This is the url name: {url_name}')
        get_tokens(soup, url_name)
        # for token, posting in token_posting.items():
        #     print(f'Token: {token}')
        #     print(f'term_doc_frequency: {posting.get_term_doc_frequency()}')
        #     print(f'url_hash: {posting.get_url_hash()}')
        #     print('------------------------------------')


def parse_json_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                parse_single_file(filepath)
                print(number_of_indexed_documents)


if __name__ == '__main__':
    parse_json_files('/Users/bryanvela/Documents/ICS121_Spring 2023_Information Retrieval/Assignment-3/DEV')
    sorted_token_posting = dict(sorted(token_posting.items()))
    for token, posting in sorted_token_posting.items():
        print(f'Token: {token}')
        print(f'term_doc_frequency: {posting.get_term_doc_frequency()}')
        print(f'url_hash: {posting.get_url_hash()}')
        print('------------------------------------')

