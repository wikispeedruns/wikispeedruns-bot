
# TODO base class

class MaxIterationsException(Exception):
    pass

class PathNotFoundException(Exception):
    pass


class GreedySearch:
    def __init__(self, embedding_provider, graph_provider, max_iterations=20):
        self.embeddings = embedding_provider
        self.graph = graph_provider
        self.max_iterations = max_iterations


    def search(start: str, end: str):
        # Greedily searches the wikipedia graph
        cur = start
        end_v = self.embeddings.get_entity_vector(end)

        visited = {start, }
        ret = [start, ]

        for i in range(self.max_iterations):
            min_dist = 2
            next_article = ""

            for link in self.graph.get_links(cur):    
                if link in visited:
                    continue

                if (link == end): 
                    #print(f"Found link in {cur}!")
                    ret += link
                    return ret

                try: 
                    cur_v = self.embeddings.get_entity_vector(link)
                except KeyError:    
                    continue

                dist = distance.cosine(cur_v, end_v)

                if dist <= min_dist:
                    next_article = link
                    min_dist = dist

            if next_article == "":
                raise PathNotFoundException("GreedySearch: could not find path")
                
            visited.add(next_article)
            cur = next_article

        raise MaxIterationsException(f"GreedySearch: Max iterations {self.max_iterations} reached, current path: {ret}")
        
