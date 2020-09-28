import requests


class search_concept:
    def __init__(self, query_word):
        self.base_url = 'http://api.conceptnet.io/c/en/'
        self.query_word = query_word

    def query_result(self):
        query_url = f'{self.base_url}{self.query_word}'
        concept_data = requests.get(query_url).json()
        return concept_data
