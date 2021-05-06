import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

endpoint = "http://localhost:7200"
repo_name = "spotify"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

PREFIXES = """prefix rdf:<http://SpotifyStats.com/rdf/>
prefix pred:<http://SpotifyStats.com/pred/>
prefix song:<http://SpotifyStats.com/song/>
prefix artist:<http://SpotifyStats.com/artist/>
prefix genre:<http://SpotifyStats.com/genre/>
prefix type:<http://SpotifyStats.com/type/>
prefix w3:<http://www.w3.org/2001/XMLSchema#>"""


def get_most_popular_songs():
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s pred:type type:song .
        ?s pred:name ?name .
        ?s pred:popularity ?pop .
        ?s pred:artists ?artist . 
        ?artist pred:name ?artist_name .
        OPTIONAL{{ ?s pred:cover_art ?cover_art }}
    }}  ORDER BY DESC(?pop) LIMIT 102
    """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']

def get_songs_by_partial_name(name):
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s pred:type type:song .
        ?s pred:name ?name .
        ?s pred:popularity ?pop .
        ?s pred:artists ?artist . 
        ?artist pred:name ?artist_name .
        OPTIONAL {{ ?s pred:cover_art ?cover_art . }}
        filter regex(?name,"{name}", "i") 
    }} ORDER BY DESC(?pop) limit 102 """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_genre_by_partial_name(name):
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s pred:type type:genre .
        ?s pred:name ?name .
        ?s pred:popularity ?pop .
        filter regex(?name,"{name}", "i") 
    }} ORDER BY DESC(?pop) limit 102 """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_artist_by_partial_name(name):
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s pred:type type:artist .
        ?s pred:name ?name .
        ?s pred:popularity ?pop .
        filter regex(?name,"{name}", "i")
    }} limit 100 """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_artist_with_genre(genre):
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s pred:type type:artist .
        ?s pred:genre genre:{genre} .
        ?s pred:name ?name .
        ?s pred:popularity ?pop .
        ?s pred:count ?count .
        OPTIONAL {{ ?s pred:face_photo ?face_photo }}
    }} ORDER BY DESC(?pop) limit 4"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_artist_genres(artist_name):
    query = f"""{PREFIXES}
    select distinct ?genre ?name where {{
        ?s pred:type type:artist .
        ?s pred:name "{artist_name}" .
        ?s pred:genre ?genre .
        ?genre pred:name ?name .
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_similar_songs_by_artists_genre(song_uri):
    query = f"""{PREFIXES}
    select distinct ?s ?name {{
        <{song_uri}> pred:artists ?artist .
        ?s pred:type type:song .
        ?artist pred:genre ?genre .
        ?s pred:artists ?art .
        ?art pred:genre ?genre .
        ?s pred:name ?name .
        filter(?s != <{song_uri}>)
    }} limit 20"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_name_of_artists_by_genre(genre_uri):
    query = f"""{PREFIXES}
    select ?s ?name where {{
        ?s pred:type type:artist .
        ?s pred:genre <{genre_uri}> .
        ?s pred:name ?name
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_name_of_artists_by_genre_name(genre_name):
    query = f"""{PREFIXES}
    select ?s ?name where {{
        ?s pred:type type:artist .
        ?genre pred:name "{genre_name}" . 
        ?s pred:genre ?genre .
        ?s pred:name ?name
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_most_popular_songs_of_artist(artist_uri):
    query = f"""{PREFIXES}
    select distinct * 
    where {{
        ?s pred:artists <{artist_uri}> .
        ?s pred:popularity ?pop
    }}  
    ORDER BY DESC(?pop) LIMIT 3"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_most_popular_artists():
    query = f"""{PREFIXES}
        select distinct * where {{
            ?s pred:type type:artist .
            ?s pred:name ?name .
            ?s pred:popularity ?pop .
        }}  ORDER BY DESC(?pop) LIMIT 100
        """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_songs_by_artist(artist_uri):
    query = f"""{PREFIXES}
    select distinct * 
    where {{
        ?s pred:artists <{artist_uri}> .
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_artist_name_by_id(id):
    query = f"""{PREFIXES}
    SELECT ?name 
    WHERE {{ 
        artist:{id} pred:name ?name
    }}
    """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_all_genres():
    query = f"""{PREFIXES}
    select distinct *
    where {{
        ?s pred:type type:genre .
        ?s pred:name ?name .
        ?s pred:popularity ?pop .
    }}  
    ORDER BY DESC(?pop) limit 102"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def describe_entity(uri):
    query = f"""SELECT * WHERE {{ <{uri}> ?p ?o }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_most_popular_songs_by_genre(genre_id):
    query = f"""{PREFIXES}
    select distinct *
    where {{
        ?s pred:artists ?art .
        ?art pred:genre genre:{genre_id} .
        ?s pred:popularity ?pop .
        ?s pred:name ?name .
        ?art pred:name ?artist_name . 
        OPTIONAL {{ ?s pred:yt_id ?yt_id . }}
        OPTIONAL {{ ?s pred:cover_art ?cover_art . }}
    }}  
    ORDER BY DESC(?pop) limit 5"""

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_similar_songs(song_id):
    query = f"""{PREFIXES}
    select * where {{ 
        song:{song_id} pred:similar ?similar .
        ?similar pred:artists ?art .
        ?similar pred:name ?name .
        ?art pred:name ?artist_name .
        OPTIONAL{{ ?similar pred:yt_id ?yt_id}}
        OPTIONAL{{ ?similar pred:cover_art ?cover_art}}
    }}"""

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_elem_count(elem):
    query = f"""{PREFIXES}
    select (Count(?s) as ?cnt) where {{ 
        ?s pred:type type:{elem} . 
    }} """

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']

# print(get_most_popular_songs_of_artist("http://SpotifyStats.com/artist/1"))
