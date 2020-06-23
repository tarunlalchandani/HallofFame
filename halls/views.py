from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video, File
from .models import Challenge
from .models import CustomUser
from .forms import CustomUserCreationForm
from .forms import VideoForm, SearchForm, CreateHallForm, CreateChallengeForm, AddFileForm
from django.forms import formset_factory
from bootstrap_datepicker_plus import DateTimePickerInput


def home(request):
    return render(request,'halls/home.html')

def allcategories(request):
    categories = Hall.objects
    return render(request,'halls/allcategories.html',{'categories':categories})

def allfiles(request):
    files = File.objects
    return render(request,'halls/allfiles.html',{'files':files})

def allchallenges(request):
    challenges = Challenge.objects
    return render(request,'halls/allchallenges.html',{'challenges':challenges})

def dashboard(request):
    return render(request,'halls/dashboard.html')

def add_video(request, pk):
    #VideoFormSet = formset_factory(VideoForm, extra=5)
    form = VideoForm()
    search_form = SearchForm()

    if request.method == 'POST':
        #Create
        filled_form = VideoFormSet(request.POST)
        if filled_form.is_valid():
            video = Video()
            video.url = filled_form.cleaned_data['url']
            video.title = filled_form.cleaned_data['title']
            video.youtube_id = filled_form.cleaned_data['youtube_id']
            video.hall = Hall.objects.get(pk = pk)
            video.save()
    return render(request, 'halls/add_video.html', {'form':form, 'search_form':search_form})

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

class CreateHall(generic.CreateView):
    form_class = CreateHallForm
    model =  Hall
    #fields = ['title','image', 'body']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        #super of class is generic CreateView
        super(CreateHall, self).form_valid(form)
        form.save()
        return redirect('dashboard')

class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'

class UpdateHall(generic.UpdateView):
    model = Hall
    template_name = 'halls/update_hall.html'
    fields = ['title','image','body']
    success_url = reverse_lazy('dashboard')

class DeleteHall(generic.UpdateView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    fields = ['title','image','body']
    success_url = reverse_lazy('dashboard')

class AddFile(generic.CreateView):
    form_class = AddFileForm
    model =  File
    template_name = 'halls/add_file.html'
    success_url = reverse_lazy('dashboard')

    def get_form(self):
        form = super().get_form()
        form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        #super of class is generic CreateView
        super(AddFile, self).form_valid(form)
        form.save()
        return redirect('dashboard')




class UpdateFile(generic.UpdateView):
    form_class = AddFileForm
    model = File
    template_name = 'halls/update_file.html'
#    fields = ['title','pub_date', 'delete_by','attachment','challenge']
    success_url = reverse_lazy('dashboard')

    def get_form(self):
        form = super().get_form()
        form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['delete_by'].widget = DateTimePickerInput()
        return form

class DeleteFile(generic.UpdateView):
    form_class = AddFileForm
    model = File
    template_name = 'halls/delete_file.html'
    #fields = ['title','pub_date', 'delete_by','attachment','challenge']
    success_url = reverse_lazy('dashboard')

    def get_form(self):
        form = super().get_form()
        form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['delete_by'].widget = DateTimePickerInput()
        return form

class DetailFile(generic.DetailView):
    model = File
    template_name = 'halls/detail_file.html'

class CreateChallenge(generic.CreateView):
    form_class = CreateChallengeForm
    model =  Challenge
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body']
    template_name = 'halls/create_challenge.html'
    success_url = reverse_lazy('dashboard')

    # #def get_form(self):
    #     form = super().get_form()
    #     form.fields['pub_date'].widget = DateTimePickerInput()
    #     form.fields['deadline_date'].widget = DateTimePickerInput()
    #     return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        #super of class is generic CreateView
        super(CreateChallenge, self).form_valid(form)
        form.save()
        return redirect('dashboard')

class DetailChallenge(generic.DetailView):
    model = Challenge
    template_name = 'halls/detail_challenge.html'

class UpdateChallenge(generic.UpdateView):
    form_class = CreateChallengeForm
    model = Challenge
    template_name = 'halls/update_challenge.html'
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body','hall']
    success_url = reverse_lazy('dashboard')

    def get_form(self):
        form = super().get_form()
        form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['deadline_date'].widget = DateTimePickerInput()
        return form

class DeleteChallenge(generic.UpdateView):
    form_class = CreateChallengeForm
    model = Challenge
    template_name = 'halls/delete_challenge.html'
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body','hall']
    success_url = reverse_lazy('dashboard')

    def get_form(self):
        form = super().get_form()
        form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['deadline_date'].widget = DateTimePickerInput()
        return form
