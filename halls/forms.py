from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from .models import Hall
from .models import File
from .models import Challenge
from bootstrap_datepicker_plus import DateTimePickerInput

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




class CreateHallForm(forms.ModelForm):

    class Meta:
        model = Hall
        fields = ['title','body','image']
        labels = {'title':'Title', 'body':'Body','image':'Image'}



class CreateChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = ['title','pub_date','deadline_date','icon','body','stipend']
        widgets = {
            'pub_date': DateTimePickerInput(),
            'deadline_date' : DateTimePickerInput(),
        }

class AddFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title','attachment']
        # widgets = {
        #     #'pub_date' : DateTimePickerInput(),
        #   # 'delete_by' : DateTimePickerInput(),
        #     'attachment' : forms.ClearableFileInput(attrs={'multiple':True})
        # }



class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='Search for Videos:')
