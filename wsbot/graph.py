from abc import ABC, abstractmethod
from wikipedia2vec import Wikipedia2Vec

import requests

class GraphProvider(ABC):
    '''
    Provide the outgoing links and other operations on the Wikipedia graph
    '''

    @abstractmethod
    def get_links(self, article):
        pass
    
    def get_links_batch(self, articles):
        return [self.get_links(a) for a in articles]


class ApiGraph(GraphProvider):
    '''
    Graph queries served by the public Wikipedia API
    '''
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "links",
        "pllimit": "max"
    }

    def __init__(self):
        pass

    def _links_from_resp(self, resp):
        links = list(resp["query"]["pages"].values())[0]["links"]
        links = [link["title"] for link in links]
        return list(filter(lambda title: ":" not in title, links))

    def get_links(self, article):
        resp = requests.get(self.URL, params={**self.PARAMS, "titles": article}).json() 
        return self._links_from_resp(resp)

    def get_links_batch(self, articles):
        # TODO figure out what happens if this returns too much
        resp = requests.get(url, params={**self.PARAMS, "titles": "|".join(articles)}).json()
        return self._links_from_resp(resp) 

# TODO database based Graph Provider
