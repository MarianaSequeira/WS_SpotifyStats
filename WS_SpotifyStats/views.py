from builtins import print
import math
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from WS_SpotifyStats.data_accessor import *
import wikipedia
import time

basename = "http://SpotifyStats.com/"


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    song_count = get_elem_count("Song")
    artist_count = get_elem_count("Artist")
    genre_count = get_elem_count("Genre")

    songs = []

    print(song_count)

    if request.method == 'POST':
        song = request.POST['song']
        artist = request.POST['artist']
        genre = request.POST['genre']
        songs = get_song_by_name_artist_genres(song, artist, genre.split(","))

    tparams = {
        'song_count': song_count[0]['cnt']['value'],
        'artist_count': artist_count[0]['cnt']['value'],
        'genre_count': genre_count[0]['cnt']['value'],
        'results': songs
    }

    return render(request, 'index.html', tparams)


def song_page(request, id):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    res = describe_entity(basename + 'spot/' + id)

    song_info = get_info(res)

    insert_recent_song(id)

    res = get_artist_name_by_id(song_info['artists'].replace("http://SpotifyStats.com/spot/", ""))
    artist_name = res[0]['name']['value']

    res = get_artist_genres(artist_name)
    artist_genre_info = get_info(res)

    similar_songs = get_similar_songs(id)

    song_list_fix = list()
    song_id_set = set()

    for song in similar_songs:
        if song['similar']['value'] not in song_id_set:
            song_list_fix.append(song)
            song_id_set.add(song['similar']['value'])


    labels = []
    data = []

    labels.append('Acousticness')
    data.append("{:.2f}".format(float(song_info.get('acousticness'))))

    labels.append('Danceability')
    data.append("{:.2f}".format(float(song_info.get('danceability'))))

    labels.append('Energy')
    data.append("{:.2f}".format(float(song_info.get('energy'))))

    labels.append('Liveness')
    data.append("{:.2f}".format(float(song_info.get('liveness'))))

    labels.append('Valence')
    data.append("{:.2f}".format(float(song_info.get('valence'))))

    duration_ms = float(song_info['duration_ms'])
    min = math.floor(duration_ms / 60000)
    seg = math.floor(duration_ms % 60000 / 1000);

    # print(song_info)

    tparams = {
        'song_info': song_info,
        'similar_songs':song_list_fix,
        'labels': labels,
        'data': data,
        'artist_name': artist_name,
        'duration': str(min) + ' min and ' + str(seg) + ' sec',
        'artist_genre_info': artist_genre_info,
    }
    return render(request, 'songPage.html', tparams)


def songs_page(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    recent_songs = get_last_seen_songs()
    print(recent_songs)

    if request.method == 'POST':
        search = request.POST['search']
        songs = get_songs_by_partial_name(search)
        title = "Songs with '" + search + "'"
    else:
        songs = get_most_popular_songs()
        title = "TOP 100"

    print(songs)

    tparams = {
        'songs': songs,
        'title': title,
        'recent_songs': recent_songs
    }

    return render(request, 'songsPage.html', tparams)


def artist_page(request, id):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    res = describe_entity(basename + 'spot/' + id)
    artist_info = get_info(res)

    res = get_artist_genres(artist_info['title'])
    artist_genre_info = get_info(res)

    res = get_most_popular_songs_of_artist(basename + 'spot/' + id)
    most_popular_songs = get_info(res)

    most_popular_songs_info = dict()

    for song in most_popular_songs.keys():
        song_info = get_info(describe_entity(song))
        most_popular_songs_info[song] = song_info


    print("\n")
    print(most_popular_songs_info)

    labels = []
    data = []

    labels.append('Acousticness')
    data.append("{:.2f}".format(float(artist_info.get('acousticness'))))

    labels.append('Danceability')
    data.append("{:.2f}".format(float(artist_info.get('danceability'))))

    labels.append('Energy')
    data.append("{:.2f}".format(float(artist_info.get('energy'))))

    labels.append('Liveness')
    data.append("{:.2f}".format(float(artist_info.get('liveness'))))

    labels.append('Valence')
    data.append("{:.2f}".format(float(artist_info.get('valence'))))
    summary = "No artist information available"
    wikipedia_url = ""

    try:
        page = wikipedia.page(artist_info['title'], auto_suggest=False)
        summary = page.summary[:400]
        wikipedia_url = page.url
    except Exception as e:
        try:
            page = wikipedia.page(artist_info['title'], auto_suggest=True)
            summary = page.summary[:400]
            wikipedia_url = page.url
        except Exception as f:
            pass
        pass

    duration_ms = float(artist_info['duration_ms'])
    min = math.floor(duration_ms / 60000)
    seg = math.floor(duration_ms % 60000 / 1000) ;

    tparams = {
        'id': id,
        'res': res,
        'artist_info': artist_info,
        'artist_genre_info': artist_genre_info,
        'most_popular_songs_info': most_popular_songs_info,
        'labels': labels,
        'summary': summary,
        'wikipedia_url': wikipedia_url,
        'data': data,
        'duration': str(min) + ' min and ' + str(seg) + ' sec'
    }

    return render(request, 'artistPage.html', tparams)


def artists_page(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        search = request.POST['search']
        artists = get_artist_by_partial_name(search)
        title = "Artists with '" + search + "'"
    else:
        artists = get_most_popular_artists()
        title = "TOP 100"

    tparams = {
        'artists': artists,
        'title': title,
    }
    return render(request, 'artistsPage.html', tparams)


def genre_page(request, id):
    res = describe_entity(basename + 'spot/' + id)
    genre_info = get_info(res)

    artists = get_artist_with_genre(id)

    print(artists)

    song_info = get_most_popular_songs_by_genre(id)

    song_list_fix = list()
    song_id_set = set()

    for song in song_info:
        if song['s']['value'] not in song_id_set:
            song_list_fix.append(song)
            song_id_set.add(song['s']['value'])

    tparams = {
        'id': id,
        'genre_info': genre_info,
        'artists': artists,
        'song_info': song_list_fix
    }

    return render(request, 'genrePage.html', tparams)


def genres_page(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    print(request)

    if request.method == 'POST':
        search = request.POST['search']
        genres = get_genre_by_partial_name(search)
        title = "Genres with '" + search + "'"
    else:
        genres = get_all_genres()
        title = "Genres"

    print(genres)

    tparams = {
        'ola': "ola",
        'title': title,
        'genres': genres
    }
    return render(request, 'genresPage.html', tparams)


def get_info(res):
    info = dict()
    for r in res:
        stable_key = ""
        for count, key in enumerate(r.keys()):
            if count == 0:
                stable_key = r[key]['value'].replace('http://SpotifyStats.com/spotp/', '').replace("http://purl.org/dc/elements/1.1/","")
                continue
            info[stable_key] = r[key]['value'].replace('http://SpotifyStats.com/spotp/', '').replace("http://purl.org/dc/elements/1.1/","")
    return info

