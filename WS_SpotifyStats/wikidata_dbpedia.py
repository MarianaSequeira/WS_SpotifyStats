from SPARQLWrapper import SPARQLWrapper2
import requests
import json
import time


def get_entity_id(searchTerm):
    searchTerm = searchTerm.replace(" ", "_")
    r = requests.get(
        f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={searchTerm}&language=en&format=json")
    data = json.loads(r.text)
    entityid = data['search'][0]['id']
    return entityid


def get_wikidata_image(entityid):
    query = f"""
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT ?image WHERE {{
            wd:{entityid} wdt:P18 ?image .
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
        }}"""
    for i in range(5):
        try:
            sparql = SPARQLWrapper2("https://query.wikidata.org/sparql")
            sparql.setQuery(query)
            return sparql.query().bindings[0]['image'].value
        except Exception as e:
            print(f"Try number {i} failed.")
    return None


def get_dbpedia_comment(entityid, name):
    query = f"""
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select distinct ?o where 
        {{
            ?s dbp:d "{entityid}"@en .
            ?s rdfs:comment ?o .
            FILTER ( LANG ( ?o ) = 'en' )
        }}"""

    for i in range(5):
        try:
            sparql = SPARQLWrapper2("https://dbpedia.org/sparql")
            sparql.setQuery(query)
            return sparql.query().bindings[0]['o'].value
        except Exception as e:
            print(f"Try number {i} failed.")
    
    query = f"""
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select distinct ?o where 
        {{
            ?s dbp:name ?name .
            ?s rdf:type schema:MusicGroup .
            ?s rdfs:comment ?o .
            filter regex(?name, "{name}", "i") 
            FILTER ( LANG ( ?o ) = 'en' )
        }}"""

    
    for i in range(5):
        try:
            sparql = SPARQLWrapper2("https://dbpedia.org/sparql")
            sparql.setQuery(query)
            return sparql.query().bindings[0]['o'].value
        except Exception as e:
            print(f"Try number {i} failed.")
    
    return None


if __name__ == '__main__':
    print(get_dbpedia_comment(get_entity_id("Ariana Grande")))
