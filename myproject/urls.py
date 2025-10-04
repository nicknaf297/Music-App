"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from app import views as main_views
from actor_artist import views as artist_view
from actor_listener import views as listener_view
from actor_admin import views as admin_view
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include
from datetime import datetime
from django.conf import settings
from django.conf.urls.static import static
from actor_listener.views import songPage, update_song_interaction


admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', main_views.home, name='home'),
    re_path(r'^contact$', main_views.contact, name='contact'),
    re_path(r'^about$', main_views.about, name='about'),
    path('login/', main_views.loginPage, name='login'),
    path('register/', main_views.registerPage, name='register'),
    re_path(r'^menu$', main_views.menu, name='menu'),
    re_path(r'^logout$',
        LogoutView.as_view(template_name = 'app/index.html'),
        name='logout'),
    
    #listener pages
    path('listenerpage/', listener_view.listenerProfile, name='listener_page'),
    path('search/', listener_view.searchPage, name='search'),
    path('song/<int:song_ID>/', listener_view.song_detail, name = 'song_detail'),
    path("song/<int:song_ID>/", songPage, name="song_page"),
    path("song/<int:song_ID>/update/", update_song_interaction, name="update_song"),
    path("listener_profile/<username>/", listener_view.searchListenerPage, name="search_listener_page"),
    path("artist_profile/<username>/", listener_view.searchArtistPage, name="search_artist_page"),
    path("liked_song_page/<username>/", listener_view.likesPage, name="liked_song_page"),
    path("song_list_page/<username>/", listener_view.songListPage, name="song_list_page"),
    

    #artist pages 
    path('artistpage/', artist_view.artistProfile, name='artist_page'),
    path('songmanagement/', artist_view.artistSongManagement, name='song_management'),
    path('createsong/', artist_view.create_song, name='create_song'),            
    path('success/', artist_view.success_page, name='success_page'),
    path('analytics/', artist_view.analyticPage, name='analytic'),
    path('songanalytics/<song_ID>', artist_view.analyticSongPage, name='song_analytic'),   #have individual page
    path('songedit/<song_ID>', artist_view.songEditPage, name='edit_song'),                #have individual page
    path('song_artist/<int:song_ID>/', artist_view.songArtistPage, name = 'song_artist_page'),

    #admin pages 
    path('adminpage/', admin_view.adminProfile, name='admin_page'),
    path('songrequest/<song_ID>', admin_view.songRequest, name='song_request'),            #have individual page
    path('approve_song/<int:song_id>/', admin_view.approve_song, name='approve_song'),
    path('reject_song/<int:song_id>/', admin_view.reject_song, name='reject_song')
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
