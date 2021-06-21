import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import time

endpoint = "http://localhost:7200"
repo_name = "spotify"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

PREFIXES = """PREFIX dc: <http://purl.org/dc/elements/1.1/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#>   
PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX spot: <http://SpotifyStats.com/spot/> 
PREFIX spotc: <http://SpotifyStats.com/spotc/> 
PREFIX spotp: <http://SpotifyStats.com/spotp/> """


def get_most_popular_songs():
    query = f"""{PREFIXES}
    select distinct ?s ?name ?pop ?cover_art (GROUP_CONCAT(DISTINCT ?artist; SEPARATOR=",") AS ?artists) (GROUP_CONCAT(DISTINCT ?artist_name ; SEPARATOR="," ) AS ?artist_names ) where {{
        ?s rdf:type spotc:Song .
        ?s dc:title ?name .
        ?s spotp:popularity ?pop .
        ?s spotp:artists ?artist . 
        ?artist dc:title ?artist_name .
            OPTIONAL{{ ?s spotp:cover_art ?cover_art }}
    }} GROUP BY ?s ?pop ?name ?cover_art ORDER BY DESC(?pop) LIMIT 102"""

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']

def get_songs_by_partial_name(name):
    query = f"""{PREFIXES}
    select distinct ?s ?name ?pop ?cover_art (GROUP_CONCAT(DISTINCT ?artist; SEPARATOR=",") AS ?artists) (GROUP_CONCAT(DISTINCT ?artist_name ; SEPARATOR="," ) AS ?artist_names ) where {{
        ?s rdf:type spotc:Song .
        ?s dc:title ?name .
        ?s spotp:popularity ?pop .
        ?s spotp:artists ?artist . 
        ?artist dc:title ?artist_name .
        OPTIONAL {{ ?s spotp:cover_art ?cover_art . }}
        filter regex(?name,"{name}", "i") 
    }} GROUP BY ?s ?pop ?name ?cover_art ORDER BY DESC(?pop) LIMIT 102 """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_genre_by_partial_name(name):
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s rdf:type spotc:Genre .
        ?s dc:title ?name .
        ?s spotp:popularity ?pop .
        filter regex(?name,"{name}", "i") 
    }} ORDER BY DESC(?pop) limit 102 """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_artist_by_partial_name(name):
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s rdf:type spotc:Artist .
        ?s dc:title ?name .
        ?s spotp:popularity ?pop .
        filter regex(?name,"{name}", "i")
    }} limit 100 """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_artist_with_genre(genre):
    query = f"""{PREFIXES}
    select distinct * where {{
        ?s rdf:type spotc:Artist .
        ?s spotp:genre spot:{genre} .
        ?s dc:title ?name .
        ?s spotp:popularity ?pop .
        ?s spotp:count ?count .
        OPTIONAL {{ ?s spotp:face_photo ?face_photo }}
    }} ORDER BY DESC(?pop) limit 4"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_artist_genres(artist_name):
    query = f"""{PREFIXES}
    select distinct ?genre ?name where {{
        ?s rdf:type spotc:Artist .
        ?s dc:title "{artist_name}" .
        ?s spotp:genre ?genre .
        ?genre dc:title ?name .
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_similar_songs_by_artists_genre(song_uri):
    query = f"""{PREFIXES}
    select distinct ?s ?name {{
        <{song_uri}> spotp:artists ?artist .
        ?s rdf:type spotc:Song .
        ?artist spotp:genre ?genre .
        ?s spotp:artists ?art .
        ?art spotp:genre ?genre .
        ?s dc:title ?name .
        filter(?s != <{song_uri}>)
    }} limit 20"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_name_of_artists_by_genre(genre_uri):
    query = f"""{PREFIXES}
    select ?s ?name where {{
        ?s rdf:type spotc:Artist .
        ?s spotp:genre <{genre_uri}> .
        ?s dc:title ?name
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_name_of_artists_by_genre_name(genre_name):
    query = f"""{PREFIXES}
    select ?s ?name where {{
        ?s rdf:type spotc:Artist .
        ?genre dc:title "{genre_name}" . 
        ?s spotp:genre ?genre .
        ?s dc:title ?name
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_most_popular_songs_of_artist(artist_uri):
    query = f"""{PREFIXES}
    select distinct * 
    where {{
        ?s spotp:artists <{artist_uri}> .
        ?s spotp:popularity ?pop
    }}  
    ORDER BY DESC(?pop) LIMIT 3"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_most_popular_artists():
    query = f"""{PREFIXES}
        select distinct * where {{
            ?s rdf:type spotc:Artist .
            ?s dc:title ?name .
            ?s spotp:popularity ?pop .
        }}  ORDER BY DESC(?pop) LIMIT 100
        """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_songs_by_artist(artist_uri):
    query = f"""{PREFIXES}
    select distinct * 
    where {{
        ?s spotp:artists <{artist_uri}> .
    }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_artist_name_by_id(id):
    query = f"""{PREFIXES}
    SELECT ?name 
    WHERE {{ 
        spot:{id} dc:title ?name
    }}
    """
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_all_genres():
    query = f"""{PREFIXES}
    select distinct *
    where {{
        ?s rdf:type spotc:Genre .
        ?s dc:title ?name .
        ?s spotp:popularity ?pop .
    }}  
    ORDER BY DESC(?pop) limit 102"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def describe_entity(uri):
    query = f"""SELECT * WHERE {{ <{uri}> ?p ?o }}"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_most_popular_songs_by_genre(genre_id):
    query = f"""{PREFIXES}
    select distinct *
    where {{
        ?s spotp:artists ?art .
        ?art spotp:genre spot:{genre_id} .
        ?s spotp:popularity ?pop .
        ?s dc:title ?name .
        ?art dc:title ?artist_name . 
        OPTIONAL {{ ?s spotp:yt_id ?yt_id . }}
        OPTIONAL {{ ?s spotp:cover_art ?cover_art . }}
    }}  
    ORDER BY DESC(?pop) limit 5"""

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_similar_songs(song_id):
    query = f"""{PREFIXES}
    select * where {{ 
        spot:{song_id} spotp:similar ?similar .
        ?similar spotp:artists ?art .
        ?similar dc:title ?name .
        ?art dc:title ?artist_name .
        OPTIONAL{{ ?similar spotp:yt_id ?yt_id}}
        OPTIONAL{{ ?similar spotp:cover_art ?cover_art}}
    }}"""

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_elem_count(elem):
    query = f"""{PREFIXES}
    select (Count(?s) as ?cnt) where {{ 
        ?s rdf:type spotc:{elem} . 
    }} """

    print(query)

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def get_song_by_name_artist_genres(song_name, artist_name, genre_list):
    genre_template_query = """
    {
        ?genre rdf:type spotc:Genre .
        ?art spotp:genre ?genre .
        ?s spotp:artists ?art .
        ?genre dc:title ?genre_name .
        filter (lcase(?genre_name)="REPLACEHERE")
    }"""
    genre_query = ""
    if genre_list[0] != '':
        genre_query += "{"
        for count, genre_name in enumerate(genre_list):
            genre_name = genre_name.strip()
            genre_query += genre_template_query.replace("REPLACEHERE", genre_name)
            if count < (len(genre_list)-1):
                genre_query += "\nUNION"
            if count == (len(genre_list) - 1):
                genre_query += "}"

    query = f"""{PREFIXES}
    
    select distinct ?s ?name ?pop ?cover_art (GROUP_CONCAT(DISTINCT ?art; SEPARATOR=", ") AS ?artists) (GROUP_CONCAT(DISTINCT ?art_name; SEPARATOR=", ") AS ?artist_names) where {{
        {{
            ?s rdf:type spotc:Song ;
                dc:title ?name ;
                spotp:popularity ?pop .
                OPTIONAL {{ ?s spotp:cover_art ?cover_art . }}
            filter regex(?name, "{song_name}", "i")
        }}
        {{
            ?art rdf:type spotc:Artist ;
                 dc:title ?art_name .
            ?s spotp:artists ?art .
            filter regex(?art_name, "{artist_name}", "i")
        }}
        {genre_query}
    }} GROUP BY ?s ?pop ?name ?cover_art ORDER BY DESC(?pop) LIMIT 9"""
    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']


def insert_recent_song(song_id):
    last_seen = int(time.time())

    query = f"""{PREFIXES}
    delete {{ ?s spotp:last_seen ?o . }}
    insert {{ ?s spotp:last_seen {last_seen} . }}
    where{{ 
        OPTIONAL {{ ?s spotp:last_seen ?o . }}
        values ?s {{ <http://SpotifyStats.com/song/{song_id}> }}
    }} """

    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query, repo_name=repo_name)




def get_last_seen_songs():
    query = f"""{PREFIXES}
    select ?s ?cover_art ?name ?pop (GROUP_CONCAT(DISTINCT ?art; SEPARATOR=", ") AS ?artists) (GROUP_CONCAT(DISTINCT ?art_name; SEPARATOR=", ") AS ?artist_names) where {{
        ?s spotp:last_seen ?p ;
           dc:title ?name ;
           spotp:artists ?art ;
           spotp:popularity ?pop .
        ?art dc:title ?art_name .
        OPTIONAL {{ ?s spotp:cover_art ?cover_art }}
    }} GROUP BY ?s ?name ?cover_art ?pop ORDER BY DESC(?p) LIMIT 3
    """

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

    res = json.loads(res)

    return res['results']['bindings']
