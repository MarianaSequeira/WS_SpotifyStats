from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from WS_SpotifyStats.data_accessor import *

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

    print(res)

    tparams = {
        'res': res,
    }
    return render(request, 'songPage.html', tparams)


def artist_page(request, id):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    res = describe_entity(basename + 'artist/' + id)

    print(res)

    info = dict()

    for resource in res:
        pred = resource['p']['value']
        obj = resource['o']['value']

        info[pred.replace('http://SpotifyStats.com/pred/', '')] = obj

    print(info)

    tparams = {
        'id': id,
        'res': res,
        'info':info
    }
    return render(request, 'artistPage.html', tparams)
