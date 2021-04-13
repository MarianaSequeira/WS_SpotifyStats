from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    tparams = {
        'ola': 'ola',
    }
    return render(request, 'index.html', tparams)
