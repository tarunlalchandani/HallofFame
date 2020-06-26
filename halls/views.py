from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from .models import Hall, File
from .models import Challenge
from .models import CustomUser
from .forms import CustomUserCreationForm
from .forms import  SearchForm, CreateHallForm, CreateChallengeForm, AddFileForm
from django.forms import formset_factory
from bootstrap_datepicker_plus import DateTimePickerInput
from django.http import Http404
import urllib
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin




def home(request):
    return render(request,'halls/home.html')


def allcategories(request):
    categories = Hall.objects
    return render(request,'halls/allcategories.html',{'categories':categories})

@login_required
def allfiles(request):
    files = File.objects
    return render(request,'halls/allfiles.html',{'files':files})

def allchallenges(request):
    challenges = Challenge.objects
    return render(request,'halls/allchallenges.html',{'challenges':challenges})

@login_required
def edashboard(request):
    halls = Hall.objects.all() #afterwards for user to filter challenges use halls = Hall.objects.filter(user=request,user)
    return render(request, 'halls/edashboard.html',{'halls':halls})

@login_required
def dashboard(request):
    return render(request,'halls/edashboard.html')


def seechallenges(request, pk):
    hall = Hall.objects.get(id = pk)
    challenges = hall.challenge_set.all()
    return render(request, 'halls/seechallenges.html',{'problems':challenges,'hall':hall})

@login_required
def seefiles(request, pk):
     challenge = Challenge.objects.get(id = pk)
     files = challenge.file_set.all()
     return render(request, 'halls/seefiles.html',{'files':files,'challenge':challenge})

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password')
        user = form.save()
        login(self.request, user, backend = 'django.contrib.auth.backends.ModelBackend')
        return view

#CRUD = Create, Read, Update, Destroy
class Login(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/login.html'

class CreateHall(LoginRequiredMixin,generic.CreateView):
    form_class = CreateHallForm
    model =  Hall
    #fields = ['title','image', 'body']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('edashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        #super of class is generic CreateView
        super(CreateHall, self).form_valid(form)
        form.save()
        return redirect('edashboard')

class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'

class UpdateHall(LoginRequiredMixin,generic.UpdateView):
    model = Hall
    template_name = 'halls/update_hall.html'
    fields = ['title','image','body']
    success_url = reverse_lazy('edashboard')

    def get_object(self):#this does not works with create and detail
        hall = super(UpdateHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall

class DeleteHall(LoginRequiredMixin, generic.UpdateView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    fields = ['title','image','body']
    success_url = reverse_lazy('edashboard')

    def get_object(self):#this does not works with create and detail
        hall = super(UpdateHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall

class AddFile(LoginRequiredMixin,generic.CreateView):
    form_class = AddFileForm
    model =  File
    template_name = 'halls/add_file.html'
    success_url = reverse_lazy('seefiles')

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.challenge_id = self.kwargs['pk']
        #super of class is generic CreateView
        super(AddFile, self).form_valid(form)
        form.save()
        return redirect('allfiles')




class UpdateFile(LoginRequiredMixin,generic.UpdateView):
    form_class = AddFileForm
    model = File
    template_name = 'halls/update_file.html'
#    fields = ['title','pub_date', 'delete_by','attachment','challenge']
    success_url = reverse_lazy('allfiles')

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        file = super(UpdateFile, self).get_object()
        if not file.challenge.hall.user == self.request.user:
            raise Http404
        return file

class DeleteFile(LoginRequiredMixin,generic.UpdateView):
    form_class = AddFileForm
    model = File
    template_name = 'halls/delete_file.html'
    #fields = ['title','pub_date', 'delete_by','attachment','challenge']
    success_url = reverse_lazy('allfiles')

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        file = super(DeleteFile, self).get_object()
        if not file.challenge.hall.user == self.request.user:
            raise Http404
        return file

class DetailFile(LoginRequiredMixin,generic.DetailView):
    model = File
    template_name = 'halls/detail_file.html'

class CreateChallenge(LoginRequiredMixin,generic.CreateView):
    form_class = CreateChallengeForm
    model =  Challenge
    template_name = 'halls/create_challenge.html'
    success_url = reverse_lazy('allchallenges')

    # def create_form(self, *args, **kwargs):
    #     form = super(CreateChallenge, self).create_form(*args, **kwargs)
    #     form.instance.user = self.request.user
    #     form.instance.hall_id = self.kwargs['pk']
    #     return form


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hall_id = self.kwargs['pk']
        #super of class is generic CreateView
        super(CreateChallenge, self).form_valid(form)
        form.save()
        return redirect('allchallenges')


class DetailChallenge(LoginRequiredMixin,generic.DetailView):
    model = Challenge
    template_name = 'halls/detail_challenge.html'

class UpdateChallenge(LoginRequiredMixin,generic.UpdateView):
    form_class = CreateChallengeForm
    model = Challenge
    template_name = 'halls/update_challenge.html'
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body','hall']
    success_url = reverse_lazy('allchallenges')

    def get_form(self):
        form = super().get_form()
        form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['deadline_date'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        challenge = super(UpdateChallenge, self).get_object()
        if not challenge.hall.user == self.request.user:
            raise Http404
        return challenge

class DeleteChallenge(LoginRequiredMixin,generic.UpdateView):
    form_class = CreateChallengeForm
    model = Challenge
    template_name = 'halls/delete_challenge.html'
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body','hall']
    success_url = reverse_lazy('allchallenges')

    def get_form(self):
        form = super().get_form()
        form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['deadline_date'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        challenge = super(DeleteChallenge, self).get_object()
        if not challenge.hall.user == self.request.user:
            raise Http404
        return challenge
