import os
import json
import re
from nltk.stem import PorterStemmer
from collections import defaultdict
from bs4 import BeautifulSoup

ALPHANUMERIC_WORDS = re.compile('[a-zA-Z0-9]+')
wordmap = {}


def parse_single_file(filename):
    # Read in the JSON data from the file
    json_data = json.load(filename)

    # Use beautifulsoup4 to remove all HTML tags
    soup = BeautifulSoup(json.dumps(json_data), 'html.parser')
    cleaned_json_data = soup.get_text()
    cleaned_json_data = soup.strip().split()
    print(cleaned_json_data)

def parse_json_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    parse_single_file(f)


def get_alphanumeric_tokens(json_data):
    alphanumeric_tokens = []
    stemmer = PorterStemmer()
    for data in json_data:
        for value in data.values():
            # Remove all non-alphanumeric characters from the value
            value = re.sub(r'\W+', ' ', value)
            # Split the value into tokens and filter out non-alphanumeric tokens
            tokens = [token for token in value.split() if token.isalnum()]
            # Apply Porter stemming to each token
            stemmed_tokens = [stemmer.stem(token) for token in tokens]
            alphanumeric_tokens.extend(stemmed_tokens)
    return alphanumeric_tokens


def count_token_frequency(tokens):
    frequency_dict = defaultdict(int)
    for token in tokens:
        frequency_dict[token] += 1
    return frequency_dict


if __name__ == '__main__':
    parse_json_folder('/Users/brandonvela/ICS121_InfoRetrieval/Milestone1/DEV/aiclub_ics_uci_edu')
    alphanumeric_tokens = get_alphanumeric_tokens(json_data)
    frequency_dict = count_token_frequency(alphanumeric_tokens)
    # Sort the tokens by frequency count, in descending order
    sorted_tokens = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)

    print("Token frequency (sorted):")
    for token, count in sorted_tokens:
        print(f"{token}: {count}")
