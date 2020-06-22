from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import Video
from .models import Hall
from .models import Challenge

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username','email')
        labels = {'username':'Your Nickname', 'email':'Enter your Email'}

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username','email')
        labels = {'username':'Your Nickname', 'email':'Enter your Email'}

class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ['title','url','youtube_id']
        labels = {'title':'Title','url':'Url','youtube_id':'YouTube Id'}

class CreateHallForm(forms.ModelForm):

    class Meta:
        model = Hall
        fields = ['title','body','image']
        labels = {'title':'Title', 'body':'Body','image':'Image'}

class CreateChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = ['title','url','pub_date','deadline_date','icon','body']
        labels = {'Title','Url','Published On','Deadline','Icon','Body'}

#class SearchForm(forms.Form):
#    search_term = forms.CharField[max_length=255, label='Search for Videos:']
