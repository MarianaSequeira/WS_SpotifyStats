import musicbrainzngs
import sys

def get_musicbrainz_img(song_id, artist, query):
    try:
        rel_id = musicbrainzngs.search_releases(query, artist=artist)['release-list'][0]['id']
        data = musicbrainzngs.get_image_list(rel_id)['images'][0]['image'].strip()
        print(f"""song:{song_id} pred:cover_art "{data}"^^w3:string . """)
    except Exception as e:
        pass

if __name__ == '__main__':
    musicbrainzngs.set_useragent("DataGather for course at University of Aveiro", "0.1", "http://SpotifyStats.com/")
    get_musicbrainz_img(sys.argv[1], sys.argv[2], sys.argv[3])
    
