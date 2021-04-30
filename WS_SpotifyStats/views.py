from builtins import print
import math
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from WS_SpotifyStats.data_accessor import *
import wikipedia
from youtube_search import YoutubeSearch

basename = "http://SpotifyStats.com/"


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    tparams = {
        'ola': "ola",
    }
    return render(request, 'index.html', tparams)


def song_page(request, id):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    res = describe_entity(basename + 'song/' + id)
    song_info = get_info(res)

    res = get_artist_name_by_id(song_info['artists'].replace("http://SpotifyStats.com/artist/", ""))
    artist_name = res[0]['name']['value']

    res = get_artist_genres(artist_name)
    artist_genre_info = get_info(res)

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

    tparams = {
        'song_info': song_info,
        'labels': labels,
        'data': data,
        'artist_name': artist_name,
        'artist_name': artist_name,
        'duration': str(min) + ' min and ' + str(seg) + ' sec',
        'artist_genre_info': artist_genre_info,
    }
    return render(request, 'songPage.html', tparams)


def artist_page(request, id):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    res = describe_entity(basename + 'artist/' + id)
    artist_info = get_info(res)

    res = get_artist_genres(artist_info['name'])
    artist_genre_info = get_info(res)

    res = get_most_popular_songs_of_artist(basename + 'artist/' + id)
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
        page = wikipedia.page(artist_info['name'])
        summary = page.summary[:400]
        wikipedia_url = page.url
    except Exception as e:
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


def genre_page(request, id):
    res = describe_entity(basename + 'genre/' + id)
    genre_info = get_info(res)

    tparams = {
        'id': id,
        'genre_info':genre_info

    }
    return render(request, 'genrePage.html', tparams)


def get_info(res):
    info = dict()
    for r in res:
        stable_key = ""
        for count, key in enumerate(r.keys()):
            if count == 0:
                stable_key = r[key]['value'].replace('http://SpotifyStats.com/pred/', '')
                continue
            info[stable_key] = r[key]['value'].replace('http://SpotifyStats.com/pred/', '')
    return info

