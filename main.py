import json
from bs4 import BeautifulSoup
import re
import os
from Posting import Posting
from porter2stemmer import Porter2Stemmer

ALPHANUMERIC_WORDS = re.compile('[a-zA-Z0-9]+')
token_posting = {}
url_docid_mapping = {}
number_of_indexed_documents = 0
doc_id_counter = 0


def is_token_in_url(word, url):    # Parse through porter too
    # Convert the token to lowercase for case-insensitive comparison
    word = word.lower()

    # Check if the URL exists in the url_docid_mapping
    if url in url_docid_mapping:
        doc_id = url_docid_mapping[url]

        # Check if the token exists in the token_posting dictionary for the specified doc_id
        if word in token_posting and doc_id in token_posting[word].doc_ids():
            return True

    return False


def is_token_in_doc(word, doc_id):  # Parse through porter too
    # Convert the token to lowercase for case-insensitive comparison
    word = word.lower()

    # Check if the token exists in the token_posting dictionary for the specified doc_id
    if word in token_posting and doc_id in token_posting[word].doc_ids():
        return True

    return False


def update_token_posting(word, doc_id):
    if word in token_posting:
        token_posting[word].update_doc_ids(doc_id)
    else:
        post = Posting()
        post.update_doc_ids(doc_id)
        token_posting[word] = post


def get_tokens(soup, doc_id) -> None:
    all_text = soup.get_text()
    all_text = all_text.strip().split()
    for word in all_text:
        word = word.lower()
        alphanum_tokens = re.findall(ALPHANUMERIC_WORDS, word)
        for w in alphanum_tokens:
            if len(w) >= 2:
                stemmer = Porter2Stemmer()
                update_token_posting(stemmer.stem(w), doc_id)


def parse_single_file(filename):
    with open(filename) as f:
        global number_of_indexed_documents, doc_id_counter

        number_of_indexed_documents += 1
        data = json.load(f)
        soup = BeautifulSoup(data['content'], 'html.parser')
        doc_id = doc_id_counter + 1
        doc_id_counter += 1

        url = data['url']  # Extract the URL from the data
        url_docid_mapping[url] = doc_id  # Save the mapping

        get_tokens(soup, doc_id)


def parse_json_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                parse_single_file(filepath)


if __name__ == '__main__':
    parse_json_files('/Users/bryanvela/Documents/ICS121_Spring 2023_Information Retrieval/Assignment-3/DEV')
    sorted_token_posting = dict(sorted(token_posting.items()))
    file = open('results.txt', 'w')
    for token, posting in sorted_token_posting.items():
        file.write(f'Token: {token}\n')
        file.write(f'Term Doc Frequency: {posting.term_doc_frequency()}\n')
        file.write(f'Doc IDs: {posting.doc_ids()}\n')
        file.write('------------------------------------\n')
    file.write(f'Number of Indexed Documents: {number_of_indexed_documents}\n')
    total_tokens = len(sorted_token_posting)
    file.write(f"Total Number of Tokens: {total_tokens}\n")
    file.close()


# Test for word in either docID or URL
    # token = "zip"
    # url = "http://alderis.ics.uci.edu/downloads.html"
    #
    # if is_token_in_url(token, url):
    #     print(f"The word '{token}' is present in the URL '{url}'.")
    # else:
    #     print(f"The word '{token}' is not present in the URL '{url}'.")

    # token = "zip"
    # doc_id = 4
    #
    # if is_token_in_doc(token, doc_id):
    #     print(f"The word '{token}' is present in doc_id {doc_id}.")
    # else:
    #     print(f"The word '{token}' is not present in doc_id {doc_id}.")

