from django.shortcuts import redirect, render, get_object_or_404
from app.models import Song, User, LikedSong, PinnedSong
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
import json

# Create your views here.
def listenerProfile(request):
    pinned_songs = Song.objects.filter(pinnedsong__user=request.user)
    return render(request, 'actor_listener/listenerpage.html', {'pinned_songs': pinned_songs})

def searchPage(request):
    if request.method == "POST":
        #what person typed in box
        search = request.POST['search']
        songs = Song.objects.filter(song_name = search, song_status='Approved')
        users = User.objects.filter(username = search)
        return render(request, 'actor_listener/searchpage.html', {'search': search, 'songs': songs, 'users': users})
    else:
        return render(request, 'actor_listener/searchpage.html')
    
def songPage(request, song_id):
    song = Song.objects.get(pk=song_id)
    return render(request, 'actor_listener/songpage.html', {"song": song})


def song_detail(request, song_ID):
    song = get_object_or_404(Song, song_ID=song_ID)
    user_has_liked = song.likedsong_set.filter(user=request.user).exists() if request.user.is_authenticated else False  # ✅ Check if user has liked
    user_has_pinned = song.pinnedsong_set.filter(user=request.user).exists() if request.user.is_authenticated else False  # ✅ Check if user has liked

    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX Request
        try:
            data = json.loads(request.body)
            action = data.get("action")
            user_has_liked = song.likedsong_set.filter(user=request.user).exists() if request.user.is_authenticated else False
            user_has_pinned = song.pinnedsong_set.filter(user=request.user).exists() if request.user.is_authenticated else False  

            if action == "like":
                liked_song, created = LikedSong.objects.get_or_create(user=request.user, song=song)

                if not created:
                    liked_song.delete()
                    liked = False
                else:
                    liked = True

                likes_count = LikedSong.objects.filter(song=song).count()

                return JsonResponse({
                    "status": "success",
                    "liked": liked,
                    "likes_count": likes_count
                })
            
            elif action == "pin":
                pinned_song, created = PinnedSong.objects.get_or_create(user=request.user, song=song)

                if not created:
                    pinned_song.delete()
                    pinned = False
                else:
                    pinned = True

                return JsonResponse({
                    "status": "success",
                    "pinned": pinned,
                })
            
            return JsonResponse({"error": "Invalid action"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return render(request, 'actor_listener/songpage.html', {
        'song': song,
        'user_has_liked': user_has_liked,
        'user_has_pinned': user_has_pinned
})


@csrf_protect
def update_song_interaction(request, song_ID):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")
            song = get_object_or_404(Song, pk=song_ID)

            if action == "like":
                liked_song, created = LikedSong.objects.get_or_create(user=request.user, song=song)

                if not created:  # If already liked, remove the like
                    liked_song.delete()
                    liked = False
                else:
                    liked = True

                likes_count = LikedSong.objects.filter(song=song).count()

                return JsonResponse({
                    "status": "success",
                    "liked": liked,
                    "likes_count": likes_count
                })
            
            elif action == "pin":
                pinned_song, created = PinnedSong.objects.get_or_create(user=request.user, song=song)

                if not created:  # If already liked, remove the like
                    pinned_song.delete()
                    pinned = False
                else:
                    pinned = True

                return JsonResponse({
                    "status": "success",
                    "pinned": pinned,
                })

            return JsonResponse({"error": "Invalid action"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def searchListenerPage(request, username):
    searchedUser = get_object_or_404(User, username=username)
    pinned_songs = Song.objects.filter(pinnedsong__user=searchedUser)
    return render(request, 'actor_listener/searchlistenerpage.html', {'searchedUser': searchedUser ,'pinned_songs': pinned_songs})

def searchArtistPage(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'actor_listener/searchartistpage.html', {'user': user})

def likesPage(request, username):
    searchUser = get_object_or_404(User, username=username)
    liked_songs = Song.objects.filter(likedsong__user=searchUser)
    return render(request, 'actor_listener/likespage.html', {'searchUser': searchUser, 'liked_songs': liked_songs})

def songListPage(request, username):
    artist = get_object_or_404(User, username=username)
    song_list = Song.objects.filter(artist_Name=username, song_status='Approved')
    return render(request, 'actor_listener/songlistpage.html', {'song_list': song_list, 'artist': artist})