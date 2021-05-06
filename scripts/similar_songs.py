import csv
import numpy as np
import threading

n3_file = open("similar_songs_thread.n3", "w")

n3_file.write("""@prefix rdf: <http://SpotifyStats.com/rdf/> . 
@prefix pred: <http://SpotifyStats.com/pred/> . 
@prefix song: <http://SpotifyStats.com/song/> . 
@prefix artist: <http://SpotifyStats.com/artist/> . 
@prefix genre: <http://SpotifyStats.com/genre/> . 
@prefix type: <http://SpotifyStats.com/type/> . 
@prefix w3: <http://www.w3.org/2001/XMLSchema#> . 

""")


data_file = open('data.csv', 'r')

song_vectors = dict()

for count, row in enumerate(csv.reader(data_file, delimiter=',')):
    if count == 0:
        continue

    song_vectors[row[6]] = [float(x) for x in [row[0], row[2], row[4], row[5], row[7], float(row[8])/11, row[9], (float(row[10])+60)/60 ,row[11], row[15],(float(row[16])-50)/100 ,row[17]]]
    
distance_songs = list()
def calculate_distance(maybe_similar_song, song):
    global song_vectors, distance_songs
    distance_songs.append((maybe_similar_song, np.linalg.norm(np.array(song_vectors[song])-np.array(song_vectors[maybe_similar_song]))))



for song in song_vectors.keys():
    distance_songs = list()
    thread_arr = list()
    for maybe_similar_song in song_vectors.keys():
        if song != maybe_similar_song:
            soma= sum(np.array(song_vectors[maybe_similar_song]))
            if soma != 0:
                while threading.activeCount() > 49:
                    continue
                t = threading.Thread(target=calculate_distance, args=[maybe_similar_song, song])
                thread_arr.append(t)
                t.start()
    for t in thread_arr:
        t.join()
    for song_id in [x[0] for x in sorted(distance_songs, key = lambda x: -x[1])[:4]]:
        n3_file.write(f"song:{song} pred:similar song:{song_id} . \n")
