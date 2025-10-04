"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Song

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
        

#Inherit UserCreationForm
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        #choose what fields to display
        fields = ['username', 'password1', 'password2', 'roles', 'profile_pic']

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    
class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_name','music_File', 'cover_image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['artist_Name'] = forms.CharField(
                initial=user.username,
                widget=forms.HiddenInput()
            )