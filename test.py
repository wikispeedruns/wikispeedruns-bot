import requests
import sys

from wikipedia2vec import Wikipedia2Vec

from scipy.spatial import distance

start = "Navigation"
end = "Barn owl"

# TODO use our data source
def get_links(article):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={article}&prop=links&pllimit=max&format=json"
    res = requests.get(url).json()
    res = list(res["query"]["pages"].values())[0]["links"]
    links = [link["title"] for link in res]
    return list(filter(lambda title: ":" not in title, links))



print("loading embeddings...")
embedding = Wikipedia2Vec.load_text("ws2vec")

cur = start
end_v = embedding.get_entity_vector(end)

visited = {start,}

for i in range(20):
    
    min_dist = 2
    next_article = ""

    for link in get_links(cur):    
        if link in visited:
            continue

        if (link == end): 
            print(f"Found link in {cur}!")
            exit(0)

        try: 
            cur_v = embedding.get_entity_vector(link)
        except KeyError:    
            continue


        dist = distance.cosine(cur_v, end_v)
        print(f"\tdistance of {link}, {end}: {dist}")

        if dist <= min_dist:
            next_article = link
            min_dist = dist

    if next_article == "":
        print(f"Could not find path")
        
    visited.add(next_article)

    print(f"Moving to {next_article}, cos dist = {min_dist}")
    cur = next_article
