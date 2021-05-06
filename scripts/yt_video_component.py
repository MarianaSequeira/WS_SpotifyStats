import threading
import json
from youtube_search import YoutubeSearch
import re
import csv

def get_yt_stuff(song_id, query):
    try:
        result_id = json.loads(YoutubeSearch(query, max_results=1).to_json())
        print(f"""song:{song_id} pred:yt_id "{result_id['videos'][0]['id']}"^^w3:string . """)
    except Exception as e:
        pass


important_songs = open("query-result.csv", "r")

imp_songs = [line.strip() for line in important_songs]

data_file = open('data.csv', 'r')

for count, row in enumerate(csv.reader(data_file, delimiter=',')):
    if count != 0:
        name = re.sub(r'"', '', row[12])
        name = re.sub(r'\\', '', name)
        song_id = row[6]
        artist_arr = row[1][2:len(row[1]) - 2]
        artist_names = list()
        if "," in artist_arr:
            artist_arr = re.split(r"['|\"], ['|\"]", artist_arr)
            for artist in artist_arr:
                artist_names.append(artist)
        else:
            artist_names.append(artist_arr)
        
        query = f"{name} {artist_names[0]}"

        if song_id in imp_songs:
            while threading.activeCount() > 4:
                continue
            t = threading.Thread(target=get_yt_stuff, args=[song_id, query.strip()])
            t.start()
