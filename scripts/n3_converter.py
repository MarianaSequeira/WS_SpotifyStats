import csv
import re
import requests
import json

general_prefix = "http://SpotifyStats.com"

# prefix for song
song_prefix = f"{general_prefix}/song"

# prefix for artist
artist_prefix = f"{general_prefix}/artist"

# prefix for predicates
predicate_prefix = f"{general_prefix}/pred"

# prefix for genre
genre_prefix = f"{general_prefix}/genre"

# prefix for type
type_prefix = f"{general_prefix}/type"

schema_prefix = "http://www.w3.org/2001/XMLSchema#"

data_file = open('data.csv', 'r')

n3_file = open('data.n3', 'w')

# chave - songID
# value - [artistIDs]
music_artists = dict()

# artistName, artistId
artists = dict()

genres = dict()

artist_count = 0

prefix_string = f"""@prefix rdf: <{general_prefix}/rdf/> .
@prefix pred: <{predicate_prefix}/> .
@prefix song: <{song_prefix}/> .
@prefix artist: <{artist_prefix}/> .
@prefix genre: <{genre_prefix}/> .
@prefix type: <{type_prefix}/> .
@prefix w3: <{schema_prefix}> ."""


n3_file.write(prefix_string)

for count, row in enumerate(csv.reader(data_file, delimiter=',')):
    if count == 0:
        continue

    song_id = row[6]

    name = re.sub(r'"', '', row[12])
    name = re.sub(r'\\', '', name)

    song_data = f'\nsong:{song_id} pred:name "{name}"^^w3:string ; '
    song_data += f'pred:type type:song ; '
    song_data += f'pred:artists '

    artist_arr = row[1][2:len(row[1]) - 2]

    string = ""

    artist_names = list()
    if "," in artist_arr:
        artist_arr = re.split(r"['|\"], ['|\"]", artist_arr)
        for artist in artist_arr:
            if artist not in artists.keys():
                artists[artist] = artist_count
                artist_count += 1
            string += f"artist:{artists[artist]}, "
            artist_names.append(artist)
        string = string[:-2]
    else:
        if artist_arr not in artists.keys():
            artists[artist_arr] = artist_count
            artist_count += 1
        artist_names.append(artist_arr)
        string += f"artist:{artists[artist_arr]}"

    song_data += f"{string} ; "
    song_data += f'pred:acousticness "{row[0]}"^^w3:double ; '
    song_data += f'pred:danceability "{row[2]}"^^w3:double ; '
    song_data += f'pred:duration_ms "{row[3]}"^^w3:integer ; '
    song_data += f'pred:energy "{row[4]}"^^w3:double ; '
    song_data += f'pred:explicit "{row[5]}"^^w3:boolean ; '
    song_data += f'pred:instrumentalness "{row[7]}"^^w3:double ; '
    song_data += f'pred:key "{row[8]}"^^w3:integer ; '
    song_data += f'pred:liveness "{row[9]}"^^w3:double ; '
    song_data += f'pred:loudness "{row[10]}"^^w3:double ; '
    song_data += f'pred:mode "{row[11]}"^^w3:boolean ; '
    song_data += f'pred:popularity "{row[13]}"^^w3:double ; '
    song_data += f'pred:release_date "{row[14]}"^^w3:date ; '
    song_data += f'pred:speechiness "{row[15]}"^^w3:double ; '
    song_data += f'pred:tempo "{row[16]}"^^w3:double ; '
    song_data += f'pred:valence "{row[17]}"^^w3:double ; '
    song_data += f'pred:year "{row[18]}"^^w3:integer .'

    n3_file.write(song_data)


genre_dict = dict()
data_by_genres_file = open('data_by_genres.csv', 'r')
for count, row in enumerate(csv.reader(data_by_genres_file, delimiter=',')):
    if count == 0:
        continue

    name = re.sub(r'"', '', row[0])
    name = re.sub(r'\\', '', name)

    genre_data = f'\ngenre:{count - 1} pred:name "{name}"^^w3:string ; '
    genre_data += f'pred:type type:genre ; '
    genre_data += f'pred:acousticness "{row[1]}"^^w3:double ; '
    genre_data += f'pred:danceability "{row[2]}"^^w3:double ; '
    genre_data += f'pred:duration_ms "{row[3]}"^^w3:integer ; '
    genre_data += f'pred:energy "{row[4]}"^^w3:double ; '
    genre_data += f'pred:instrumentalness "{row[5]}"^^w3:double ; '
    genre_data += f'pred:key "{row[12]}"^^w3:integer ; '
    genre_data += f'pred:liveness "{row[6]}"^^w3:double ; '
    genre_data += f'pred:loudness "{row[7]}"^^w3:double ; '
    genre_data += f'pred:mode "{row[13]}"^^w3:boolean ; '
    genre_data += f'pred:popularity "{row[11]}"^^w3:double ; '
    genre_data += f'pred:speechiness "{row[8]}"^^w3:double ; '
    genre_data += f'pred:tempo "{row[9]}"^^w3:double ; '
    genre_data += f'pred:valence "{row[10]}"^^w3:double .'

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

    artist_data = f'\nartist:{artists[row[0]]} pred:name "{name}"^^w3:string ; '
    artist_data += f'pred:type type:artist ; '
    artist_data += f'pred:acousticness "{row[1]}"^^w3:double ; '
    artist_data += f'pred:danceability "{row[2]}"^^w3:double ; '
    artist_data += f'pred:duration_ms "{row[3]}"^^w3:integer ; '
    artist_data += f'pred:energy "{row[4]}"^^w3:double ; '
    artist_data += f'pred:instrumentalness "{row[5]}"^^w3:double ; '
    artist_data += f'pred:key "{row[12]}"^^w3:integer ; '
    artist_data += f'pred:liveness "{row[6]}"^^w3:double ; '
    artist_data += f'pred:loudness "{row[7]}"^^w3:double ; '
    artist_data += f'pred:mode "{row[13]}"^^w3:boolean ; '
    artist_data += f'pred:popularity "{row[11]}"^^w3:double ; '
    artist_data += f'pred:speechiness "{row[8]}"^^w3:double ; '
    artist_data += f'pred:tempo "{row[9]}"^^w3:double ; '
    artist_data += f'pred:valence "{row[10]}"^^w3:double ; '
    artist_data += f'pred:count "{row[14]}"^^w3:integer ; '

    string = ""

    genre_arr = row[15][2:len(row[15]) - 2]

    if genre_arr != "":
        if "," in row[15]:
            genre_arr = re.split(r"['|\"], ['|\"]", genre_arr)
            for genre in genre_arr:
                string += f"genre:{genre_dict[genre]}, "
            string = string[:-2]
        else:
            string += f"genre:{genre_dict[genre_arr]}"
    if string != "":
        artist_data += f'pred:genre {string} .'
    else:
        artist_data = artist_data[:-2] + ". "

    n3_file.write(artist_data)

n3_file.close()
