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
from django.contrib import messages



def home(request):
    recent_category = Hall.objects.all().order_by('-id')[:5]
    recent_challenges = Challenge.objects.all().order_by('-id')[:10]
    deadline_challenges = Challenge.objects.all().order_by('-deadline_date')
    return render(request,'halls/home.html', {'recent_category':recent_category,'recent_challenges':recent_challenges,'deadline_challenges':deadline_challenges})



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
    #success_url = reverse_lazy('edashboard')

    def get_success_url(self):
        s = 'Category'+ self.object.title + ' created successfully'
        messages.add_message(self.request, messages.INFO, s)
        return reverse_lazy('edashboard')

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
    #success_url = reverse_lazy('edashboard')

    def get_success_url(self):
        s = 'Category'+ self.object.title + ' updated successfully'
        messages.add_message(self.request, messages.INFO, s)
        return reverse_lazy('edashboard')

    def get_object(self):#this does not works with create and detail
        hall = super(UpdateHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall

class DeleteHall(LoginRequiredMixin, generic.UpdateView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    fields = ['title','image','body']
    #success_url = reverse_lazy('edashboard')

    def get_success_url(self):
        s = 'Category'+ self.object.title + ' deleted successfully'
        messages.add_message(self.request, messages.INFO, s)
        return reverse_lazy('edashboard')

    def get_object(self):#this does not works with create and detail
        hall = super(UpdateHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall

class AddFile(LoginRequiredMixin,generic.CreateView):
    form_class = AddFileForm
    model =  File
    template_name = 'halls/add_file.html'
    # success_url = "/add_file_completed/"

    def get_success_url(self):
        s = 'file '+ self.object.title + ' added successfully'
        messages.add_message(self.request, messages.INFO, s)
        challenge = self.object.challenge
        return reverse_lazy('seefiles', kwargs = {'pk':challenge.pk })

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
        return super().form_valid(form)




class UpdateFile(LoginRequiredMixin,generic.UpdateView):
    form_class = AddFileForm
    model = File
    template_name = 'halls/update_file.html'
#    fields = ['title','pub_date', 'delete_by','attachment','challenge']
    # success_url = "/update_file_completed/"

    def get_success_url(self):
        s = 'file ' + self.object.title + ' updated successfully'
        messages.add_message(self.request, messages.INFO, s)
        challenge = self.object.challenge
        return reverse_lazy('seefiles', kwargs = {'pk':challenge.pk })

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

class DeleteFile(LoginRequiredMixin,generic.DeleteView):
    form_class = AddFileForm
    model = File
    template_name = 'halls/delete_file.html'
    #fields = ['title','pub_date', 'delete_by','attachment','challenge']
    def get_success_url(self):
        s = 'file '+ self.object.title +' deleted successfully'
        messages.add_message(self.request, messages.INFO, s)
        challenge = self.object.challenge
        return reverse_lazy('seefiles', kwargs = {'pk':challenge.pk })

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
    # success_url = "/create_challenge_completed/"

    def get_success_url(self):
        s = 'challenge ' + self.object.title + ' created successfully'
        messages.add_message(self.request, messages.INFO, s)
        hall = self.object.hall
        return reverse_lazy('seechallenges', kwargs = {'pk':hall.pk })
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
        return super().form_valid(form)


class DetailChallenge(LoginRequiredMixin,generic.DetailView):
    model = Challenge
    template_name = 'halls/detail_challenge.html'

class UpdateChallenge(LoginRequiredMixin,generic.UpdateView):
    form_class = CreateChallengeForm
    model = Challenge
    template_name = 'halls/update_challenge.html'
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body','hall']

    def get_success_url(self):
        s = 'challenge '+ self.object.title + ' updated successfully'
        messages.add_message(self.request, messages.INFO, s)
        hall = self.object.hall
        return reverse_lazy('seechallenges',kwargs = {'pk':hall.pk })

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

class DeleteChallenge(LoginRequiredMixin,generic.DeleteView):
    form_class = CreateChallengeForm
    model = Challenge
    template_name = 'halls/delete_challenge.html'
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body','hall']
    # success_url = "/delete_challenge_completed/"

    def get_success_url(self):
        s = 'challenge '+ self.object.title + ' deleted successfully'
        messages.add_message(self.request, messages.INFO, s)
        hall = self.object.hall
        return reverse_lazy('seechallenges', kwargs = {'pk':hall.pk })

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
