import threading
import json
import requests
import wikipedia

def get_wikimedia_img(artist_id, query):
    try:
        url = None
        try:
            wiki_page = wikipedia.page("query", auto_suggest=True)
            url = f"https://en.wikipedia.org/w/api.php?action=query&titles={wiki_page.title}&prop=pageimages&pithumbsize=300&format=json"
        except Exception as e:
            try:
                wiki_page = wikipedia.page("query", auto_suggest=False)
                url = f"https://en.wikipedia.org/w/api.php?action=query&titles={wiki_page.title}&prop=pageimages&pithumbsize=300&format=json"
            except Exception as d:
                url = f"https://en.wikipedia.org/w/api.php?action=query&titles={query}&prop=pageimages&pithumbsize=300&format=json"

        json_data = json.loads(requests.get(url).text)
        source = [x['thumbnail']['source'] for x in json_data['query']['pages'].values()][0]
        print(f"""artist:{artist_id} pred:face_photo "{source}"^^w3:string . """)
    except Exception as e:
        pass


fl = open("artist_search.tsv", "r")

for count, line in enumerate(fl):
    if count != 0:
        query, artist_id = tuple(line.split("\t"))
        while threading.activeCount() > 25:
            continue
        t = threading.Thread(target=get_wikimedia_img, args=[artist_id.strip(), query.strip()])
        t.start()
