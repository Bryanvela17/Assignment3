class Posting:
    def __init__(self):
        self._term_doc_frequency = 0
        self._doc_ids = set()
        self._url_count = 0

    def update_term_doc_frequency(self):
        self._term_doc_frequency = self._url_count

    def update_doc_ids(self, doc_id):
        if doc_id not in self._doc_ids:
            self._doc_ids.add(doc_id)
            self._url_count += 1
            self.update_term_doc_frequency()

    def remove_doc_id(self, doc_id):
        if doc_id in self._doc_ids:
            self._doc_ids.remove(doc_id)
            self._url_count -= 1
            self.update_term_doc_frequency()

    def term_doc_frequency(self):
        return self._term_doc_frequency

    def doc_ids(self):
        return self._doc_ids

    def url_count(self):
        return self._url_count
