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
        ?s pred:popularity ?pop
    }}  ORDER BY DESC(?pop) LIMIT 100
    """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_song_count():
    query = f"""{PREFIXES}
    select (count(?s) as ?count) where {{ 
        ?s pred:type type:song .
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_song_by_partial_name(name):
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s pred:type type:song .
        ?s pred:name ?name .
        filter regex(?name,"{name}", "i")
    }} limit 100 """
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
        filter regex(?name,"{name}", "i")
    }} limit 100 """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


def get_artist_with_genre(genre):
    query = f"""{PREFIXES}
    select distinct ?s ?name where {{
        ?s pred:type type:artist .
        ?s pred:genre genre:{genre} .
        ?s pred:name ?name
    }}"""
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
    }} limit 100"""
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


def describe_entity(uri):
    query = f"""SELECT * WHERE {{ <{uri}> ?p ?o }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    accessor.sparql_select()
    res = json.loads(res)

    return res['results']['bindings']


# GET MOST POPULAR SONGS OF ARTIST (artist_uri)

print(describe_entity("http://SpotifyStats.com/song/2DFRFqWNahKtFD112H2iEZ"))
