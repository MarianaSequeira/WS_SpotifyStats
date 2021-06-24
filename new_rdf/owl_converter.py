import csv
import re
import requests
import json

general_prefix = "http://SpotifyStats.com"

schema_prefix = "http://www.w3.org/2001/XMLSchema#"

data_file = open('data.csv', 'r')

n3_file = open('data.n3', 'w')

music_artists = dict()

artists = dict()

genres = dict()

artist_count = 0

with open("ontology_def.n3", "r") as ont_prefix:
    for line in ont_prefix:
        n3_file.write(line)

for count, row in enumerate(csv.reader(data_file, delimiter=',')):
    if count == 0:
        continue

    song_id = row[6]

    name = re.sub(r'"', '', row[12])
    name = re.sub(r'\\', '', name)

    song_data = f'\nspot:s{song_id} dc:title "{name}"^^w3:string ; '
    song_data += f'spotp:artists '

    artist_arr = row[1][2:len(row[1]) - 2]

    string = ""

    artist_names = list()
    if "," in artist_arr:
        artist_arr = re.split(r"['|\"], ['|\"]", artist_arr)
        for artist in artist_arr:
            if artist not in artists.keys():
                artists[artist] = artist_count
                artist_count += 1
            string += f"spot:a{artists[artist]}, "
            artist_names.append(artist)
        string = string[:-2]
    else:
        if artist_arr not in artists.keys():
            artists[artist_arr] = artist_count
            artist_count += 1
        artist_names.append(artist_arr)
        string += f"spot:a{artists[artist_arr]}"

    song_data += f"{string} ; "
    song_data += f'spotp:acousticness "{row[0]}"^^w3:double ; '
    song_data += f'spotp:danceability "{row[2]}"^^w3:double ; '
    song_data += f'spotp:duration_ms "{row[3]}"^^w3:double ; '
    song_data += f'spotp:energy "{row[4]}"^^w3:double ; '
    song_data += f'spotp:explicit "{row[5]}"^^w3:boolean ; '
    song_data += f'spotp:instrumentalness "{row[7]}"^^w3:double ; '
    song_data += f'spotp:liveness "{row[9]}"^^w3:double ; '
    song_data += f'spotp:loudness "{row[10]}"^^w3:double ; '
    song_data += f'spotp:mode "{row[11]}"^^w3:boolean ; '
    song_data += f'spotp:popularity "{row[13]}"^^w3:double ; '
    song_data += f'spotp:release_date "{row[14]}"^^w3:string ; '
    song_data += f'spotp:speechiness "{row[15]}"^^w3:double ; '
    song_data += f'spotp:tempo "{row[16]}"^^w3:double ; '
    song_data += f'spotp:valence "{row[17]}"^^w3:double ; '
    song_data += f'spotp:year "{row[18]}"^^w3:integer .'

    n3_file.write(song_data)


genre_dict = dict()
data_by_genres_file = open('data_by_genres.csv', 'r')
for count, row in enumerate(csv.reader(data_by_genres_file, delimiter=',')):
    if count == 0:
        continue

    name = re.sub(r'"', '', row[0])
    name = re.sub(r'\\', '', name)

    genre_data = f'\nspot:g{count - 1} dc:title "{name}"^^w3:string ; '
    genre_data += f'spotp:acousticness "{row[1]}"^^w3:double ; '
    genre_data += f'spotp:danceability "{row[2]}"^^w3:double ; '
    genre_data += f'spotp:duration_ms "{row[3]}"^^w3:double ; '
    genre_data += f'spotp:energy "{row[4]}"^^w3:double ; '
    genre_data += f'spotp:instrumentalness "{row[5]}"^^w3:double ; '
    genre_data += f'spotp:key "{row[12]}"^^w3:integer ; '
    genre_data += f'spotp:liveness "{row[6]}"^^w3:double ; '
    genre_data += f'spotp:loudness "{row[7]}"^^w3:double ; '
    genre_data += f'spotp:mode "{row[13]}"^^w3:boolean ; '
    genre_data += f'spotp:popularity "{row[11]}"^^w3:double ; '
    genre_data += f'spotp:speechiness "{row[8]}"^^w3:double ; '
    genre_data += f'spotp:tempo "{row[9]}"^^w3:double ; '
    genre_data += f'spotp:valence "{row[10]}"^^w3:double .'

    genre_dict[row[0]] = count - 1

    n3_file.write(genre_data)

data_by_artist_file = open('data_w_genres.csv', 'r')

for count, row in enumerate(csv.reader(data_by_artist_file, delimiter=',')):
    if count == 0:
        continue
    if row[0] not in artists.keys():
        continue

    name = re.sub(r'"', '', row[0])
    name = re.sub(r'\\', '', name)
    name = re.sub(r"”", '', name)

    artist_data = f'\nspot:a{artists[row[0]]} dc:title "{name}"^^w3:string ; '
    artist_data += f'spotp:acousticness "{row[1]}"^^w3:double ; '
    artist_data += f'spotp:danceability "{row[2]}"^^w3:double ; '
    artist_data += f'spotp:duration_ms "{row[3]}"^^w3:double ; '
    artist_data += f'spotp:energy "{row[4]}"^^w3:double ; '
    artist_data += f'spotp:instrumentalness "{row[5]}"^^w3:double ; '
    artist_data += f'spotp:liveness "{row[6]}"^^w3:double ; '
    artist_data += f'spotp:loudness "{row[7]}"^^w3:double ; '
    artist_data += f'spotp:mode "{row[13]}"^^w3:boolean ; '
    artist_data += f'spotp:popularity "{row[11]}"^^w3:double ; '
    artist_data += f'spotp:speechiness "{row[8]}"^^w3:double ; '
    artist_data += f'spotp:tempo "{row[9]}"^^w3:double ; '
    artist_data += f'spotp:valence "{row[10]}"^^w3:double ; '
    artist_data += f'spotp:count "{row[14]}"^^w3:integer ; '

    string = ""

    genre_arr = row[15][2:len(row[15]) - 2]

    if genre_arr != "":
        if "," in row[15]:
            genre_arr = re.split(r"['|\"], ['|\"]", genre_arr)
            for genre in genre_arr:
                string += f"spot:g{genre_dict[genre]}, "
            string = string[:-2]
        else:
            string += f"spot:g{genre_dict[genre_arr]}"
    if string != "":
        artist_data += f'spotp:genre {string} .'
    else:
        artist_data = artist_data[:-2] + ". "

    n3_file.write(artist_data)


with open("cover_art.n3", "r") as cover_art_file:
    for line in cover_art_file:
        n3_file.write(line)


with open("yt_videoid.n3", "r") as yt_videoid:
    for line in yt_videoid:
        n3_file.write(line)


with open("similar_songs.n3", "r") as similar_songs:
    for line in similar_songs:
        n3_file.write(line)


n3_file.close()
