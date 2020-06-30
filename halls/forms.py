from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.db import transaction
from .models import Hall
from .models import File
from .models import Tutor
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

class EmployeeSignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username','email')
        labels = {'username':'Your Nickname', 'email':'Enter your Email'}

    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_employee = True
        if commit:
            user.save()
        return user

class TutorSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset = Hall.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = True
    )

    class Meta:
        model = CustomUser
        fields = ('username','email')
        labels = {'username':'Your Nickname', 'email':'Enter your Email'}

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tutor = True
        user.save()
        tutor = Tutor.objects.create(user=user)
        tutor.interests.add(*self.cleaned_data.get('interests'))
        return user
