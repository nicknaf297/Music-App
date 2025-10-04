from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from app.forms import SongForm
from app.models import Song, LikedSong, PinnedSong, User
from django.db.models import Count

# Create your views here.
def artistProfile(request):
    return render(request, 'actor_artist/artistpage.html')

def artistSongManagement(request):
    song_list = Song.objects.filter(artist_Name=request.user.username)
    return render(request, 'actor_artist/artistsongmanagement.html', {'song_list': song_list})

def create_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            song = form.save(commit = False)
            song.artist_Name = request.user.username
            song.save()
            return redirect('success_page')
    else:
        form = SongForm(user=request.user)

    return render(request, 'actor_artist/createsongpage.html', {'form': form})

def success_page(request):
    return render(request, 'actor_artist/success.html')

def analyticPage(request):
    song_list = Song.objects.filter(artist_Name=request.user.username, song_status='Approved')
    total_likes = LikedSong.objects.filter(song__artist_Name=request.user.username).count()
    total_pins = PinnedSong.objects.filter(song__artist_Name=request.user.username).count()
    most_liked_song = (
        Song.objects.filter(artist_Name=request.user.username)
        .annotate(total_likes=Count('liked_by'))
        .order_by('-total_likes')
        .first()
    )
    
    context = {
        "song_list": song_list,
        "total_likes": total_likes,
        "total_pins": total_pins,
        "most_liked_song": most_liked_song,
    }
    return render(request, 'actor_artist/analyticspage.html', context)

def analyticSongPage(request, song_ID):
    song = get_object_or_404(Song, pk=song_ID)
    total_likes = LikedSong.objects.filter(song=song).count()
    total_pins = PinnedSong.objects.filter(song=song).count()
    users_liked = User.objects.filter(likedsong__song=song)
    users_pinned = User.objects.filter(pinnedsong__song=song)

    context = {
        "song": song,
        "users_liked": users_liked,
        "users_pinned": users_pinned,
        "total_likes": total_likes,
        "total_pins": total_pins
    }

    return render(request, 'actor_artist/songanalyticspage.html', context)

def songEditPage(request, song_ID):
    song = get_object_or_404(Song, song_ID = song_ID)
    if request.method == 'POST':
        song.song_name = request.POST.get('song_name')
        if 'cover_image' in request.FILES:
            song.cover_image = request.FILES['cover_image']
            song.save()
            return redirect('song_management')
    return render(request, 'actor_artist/editsong.html', {'song': song})

def songArtistPage(request, song_ID):
    song = get_object_or_404(Song, song_ID=song_ID)
    return render(request, 'actor_artist/songartistpage.html', {'song': song})