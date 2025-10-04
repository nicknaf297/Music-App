"""
Definition of models.
"""
#add models in admin.py

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

#sharing entity

class User(AbstractUser):
    role_choices = (('Listener', 'Listener'),
        ('Artist', 'Artist'),
        ('Admin', 'Admin'),)
    roles = models.CharField(max_length= 10, choices=role_choices, default='Listener')
    profile_pic = models.ImageField(upload_to='userPictures/', default='userPictures/default.jpg')
    liked_songs = models.ManyToManyField('Song', through='LikedSong', related_name='liked_by')
    pinned_songs = models.ManyToManyField('Song', through='PinnedSong', related_name='pinned_by')

class Song(models.Model):
    STATUS_CHOICES = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Not Approved', 'Not Approved'),)
    song_ID = models.AutoField(primary_key=True)
    song_name = models.TextField()
    music_File = models.FileField(upload_to='songs/', validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    artist_Name = models.TextField()
    cover_image = models.ImageField(upload_to='songPictures/', default='songPictures/default.jpg')
    song_status = models.CharField(max_length = 15, choices = STATUS_CHOICES, default = 'Pending')
    def __str__(self):
        return f"{self.song_name} by {self.artist_Name} - ({self.song_status})"

class LikedSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user','song')

class PinnedSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user','song')