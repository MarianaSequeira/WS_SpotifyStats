"""WS_SpotifyStats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from WS_SpotifyStats import views

urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.songs_page, name='songs'),
    path('song/<str:id>/', views.song_page, name='song'),
    path('artist/<str:id>/', views.artist_page, name='artist'),
    path('artists/', views.artists_page, name='artists'),
    path('decades/', views.decades, name='decades'),
    path('genre/<str:id>/', views.genre_page, name='genre'),
    path('genres', views.genres_page, name='genres'),
    path('stats/', views.home, name='stats'),

    path('admin/', admin.site.urls),

]