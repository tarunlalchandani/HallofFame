from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.db import transaction
from .models import Hall
from .models import File
from .models import Payment
from .models import Solution
from .models import Profile
from .models import Challenge
from .models import Request
from bootstrap_datepicker_plus import DateTimePickerInput

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username','email','is_tutor','is_employee')
        labels = {'username':'Your Nickname', 'email':'Enter your Email'}


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username','email','is_tutor','is_employee')
        labels = {'username':'Your Nickname', 'email':'Enter your Email'}



class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = {'FirstName','LastName','WhatsappNumber','Skills','University','Branch','Year','Resume','upiId','AccountNumber','BeneficiaryName','IFSC','Other_Details'}
        labels = {'FirstName':'FirstName*','LastName':'LastName*','WhatsappNumber':'WhatsappNumber*','Skills':'Skills*','University':'University','Branch':'Branch','Year':'ExperienceInYears','Resume':'Resume','upiId':'upiId','AccountNumber':'AccountNumber','BeneficiaryName':'BeneficiaryName','IFSC':'IFSC','Other_Details':'Give a short Introduction'}


        def save(self,commit=True):
            user = super().save(commit=False)
            user.rating = '0'
            user.money_earned = 0
            if commit:
                user.save()
            return user
    field_order = ['FirstName','LastName','WhatsappNumber','Skills','University','Branch','Year','Resume','upiId','AccountNumber','BeneficiaryName','IFSC','Other_Details']
        #not taken rating, money_earned as we will see to it decided by the employee



class CreateHallForm(forms.ModelForm):

    class Meta:
        model = Hall
        fields = ['title','body','image']
        labels = {'title':'Title', 'body':'Body','image':'Image'}



class CreateChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = ['title','deadline_date','body','stipend','type']
        widgets = {
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

class AddSolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['ans','solutionfile']

class AddPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_details','payment_file']

class RequestChallengeForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['HowToSolve']
        labels = {'HowToSolve':'How You are going to Solve It'}


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
        user.is_tutor = False
        if commit:
            user.save()
        return user

class TutorSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email')
        labels = {'username':'Your Nickname', 'email':'Enter your Email'}

    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_tutor = True
        user.is_employee = False
        if commit:
            user.save()
        return user
