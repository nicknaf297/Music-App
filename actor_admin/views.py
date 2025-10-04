from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from app.models import Song

# Create your views here.
def adminProfile(request):
    pending_songs = Song.objects.filter(song_status= 'Pending')
    return render(request, 'actor_admin/adminpage.html', {'pending_songs': pending_songs})

def songRequest(request, song_ID):
    song = get_object_or_404(Song, song_ID=song_ID)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        song.song_status = new_status
        song.save()
        return redirect('admin_page')
    return render(request, 'actor_admin/songrequest.html', {'song': song})

def approve_song(request, song_id):
    song = get_object_or_404(Song, song_ID=song_id)
    song.song_status = 'Approved'
    song.save()
    return redirect('admin_page')

def reject_song(request, song_id):
    song = get_object_or_404(Song, song_ID=song_id)
    song.song_status = 'Not Approved'
    song.save()
    return redirect('admin_page')