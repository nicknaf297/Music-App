from django.contrib import admin
from app.models import User, Song, LikedSong, PinnedSong

admin.site.register(User)
admin.site.register(Song)
admin.site.register(LikedSong)
admin.site.register(PinnedSong)