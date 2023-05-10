from nltk.tokenize import RegexpTokenizer

#regTokenizer = RegexpTokenizer(r'\w+')

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
def parseFile():
    pass


def run():
    pass

if __name__ == '__main__':
    run()