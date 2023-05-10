class Posting:
    def __init__(self):
        self.term_doc_frequency = 0
        self.url_hash = []

    def update_term_doc_frequency(self):
        self.term_doc_frequency = len(self.url_hash)

    def update_url_hash(self, url):
        if url not in self.url_hash:
            self.url_hash.append(url)
            self.update_term_doc_frequency()

    def get_term_doc_frequency(self):
        return self.term_doc_frequency

    def get_url_hash(self):
        return self.url_hash

