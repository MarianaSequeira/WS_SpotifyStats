from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from WS_SpotifyStats.data_accessor import *
import wikipedia

basename = "http://SpotifyStats.com/"


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    tparams = {
        'ola': "ola",
    }
    return render(request, 'index.html', tparams)


def song_page(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    res = describe_entity("http://SpotifyStats.com/song/2DFRFqWNahKtFD112H2iEZ")

    tparams = {
        'res': res,
    }
    return render(request, 'songPage.html', tparams)


def artist_page(request, id):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    res = describe_entity(basename + 'artist/' + id)
    artist_info = get_info(res)

    res = get_artist_genres(artist_info['name'])
    artist_genre_info = get_info(res)

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

    try:
        summary = wikipedia.summary(artist_info['name'], chars=400)
    except Exception as e:
        pass

    tparams = {
        'id': id,
        'res': res,
        'artist_info': artist_info,
        'artist_genre_info': artist_genre_info,
        'labels': labels,
        'summary': summary,
        'data': data,
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

    print(info)
    return info

