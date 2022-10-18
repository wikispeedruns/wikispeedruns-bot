from abc import ABC, abstractmethod
from wikipedia2vec import Wikipedia2Vec

class GraphProvider(ABC):
    '''
    Provide the outgoing links and other operations on the Wikipedia graph
    '''

    @abstractmethod
    def get_links(self, article: str):
        pass
    
    def get_links_batch(self, articles: list[str]):
        return [self.get_links(a) for a in articles]
            
class ApiGraph(GraphProvider):
    '''
    Graph queries served by the public Wikipedia API
    '''
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json"
        "prop": "links"
        "pllinmit": "max"
    }

    def __init__(self.filename: str):
        self.wiki2vec = Wikipedia2Vec.load_text(filename)

    def _links_from_resp(resp)
        links = list(res["query"]["pages"].values())[0]["links"]
        links = [link["title"] for link in ret]
        return list(filter(lambda title: ":" not in title, links))


    def get_links(self, article: str):
        resp = requests.get(url, params={**self.PARAMS, "title": article}).json()
        return _links_from_resp(resp)

    def get_links_batch(self, articles: list[str]):
        resp = requests.get(url, params={**self.PARAMS, "title": "|".join(articles)}).json()
        return _links_from_resp(resp) 

# TODO database based Graph Provider
