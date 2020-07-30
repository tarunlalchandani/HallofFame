from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from .models import Hall, File, Request, Solution, Payment
from .models import Challenge
from .models import Profile
from .models import CustomUser
from .forms import CustomUserCreationForm
from .forms import  SearchForm, CreateHallForm, CreateChallengeForm, AddFileForm, AddSolutionForm, AddPaymentForm, TutorSignUpForm, EmployeeSignUpForm, CreateProfileForm, RequestChallengeForm
from django.forms import formset_factory
from bootstrap_datepicker_plus import DateTimePickerInput
from django.http import Http404
import urllib
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from .decorators import tutor_required, employee_required
#loginemailsuperuser=new@gmail.com password gnew@2020
from datetime import date
from django.db.models import Q
def home(request):
    recent_category = Hall.objects.all().order_by('-id')[:8]
    recent_projects = Challenge.objects.all().filter(type='P')[:8]
    recent_assignments = Challenge.objects.all().filter(type='A')[:8]
    recent_TimeBoundChallenges = Challenge.objects.all().filter(type='T')[:8]
    deadline_challenges = Challenge.objects.all().order_by('-deadline_date')
    return render(request,'halls/home.html', {'recent_category':recent_category,'recent_projects':recent_projects,'recent_assignments':recent_assignments,'recent_TimeBoundChallenges':recent_TimeBoundChallenges})

def signup(request):
    return render(request,'registration/signup.html')


def allcategories(request):
    categories = Hall.objects
    return render(request,'halls/allcategories.html',{'categories':categories})


def allprojects(request):
    challenges = Challenge.objects.all().filter(type='P')
    return render(request,'halls/allchallenges.html',{'challenges':challenges,'section_title':"Projects"})


def allassignments(request):
    challenges = Challenge.objects.all().filter(type='A')
    return render(request,'halls/allchallenges.html',{'challenges':challenges,'section_title':"Assignments"})

def allTimeBoundChallenges(request):
    challenges = Challenge.objects.all().filter(type='T')
    return render(request,'halls/allchallenges.html',{'challenges':challenges,'section_title':"TimeBoundChallenges"})



@login_required
@employee_required
def allfiles(request):
    files = File.objects
    return render(request,'halls/allfiles.html',{'files':files})

@login_required
@employee_required
def allsolutions(request):
    solutions = Solution.objects
    return render(request,'halls/allsolutions.html',{'solutions':solutions})

@login_required
@employee_required
def allpayments(request):
    payments = Payment.objects
    return render(request,'halls/allpayments.html',{'payments':payments})


@login_required
@employee_required
def allrequests(request):
    allrequests = Request.objects.order_by('tutorId')
    return render(request,'halls/allrequests.html',{'allrequests':allrequests})


def allchallenges(request):
    challenges = Challenge.objects
    if request.method == 'POST':
        KeywordSearch = request.POST['KeywordSearch']
        criteria1 = Q(title__contains=KeywordSearch)
        criteria2 = Q(body__contains=KeywordSearch)
        challenges = Challenge.objects.all().filter(criteria1 | criteria2)
        return render(request,'halls/allchallenges.html',{'challenges':challenges,'section_title':'Search:KeywordSearch'})
    return render(request,'halls/allchallenges.html',{'challenges':challenges,'section_title':"All Challenges"})

@login_required
@employee_required
def edashboard(request):
    halls = Hall.objects.all() #afterwards for user to filter challenges use halls = Hall.objects.filter(user=request,user)
    return render(request, 'halls/edashboard.html',{'halls':halls})

@login_required
@tutor_required
def dashboard(request):
    username = request.user.username
    requests = Request.objects.filter(tutorName=username)

    return render(request,'halls/dashboard.html',{'requests':requests})


def seechallenges(request, pk):
    hall = Hall.objects.get(id = pk)
    challenges = hall.challenge_set.all()
    return render(request, 'halls/seechallenges.html',{'problems':challenges,'hall':hall})





@login_required
def seefiles(request, pk):
     hide = True
     requested = False
     challenge = Challenge.objects.get(id = pk)
     files = challenge.file_set.all()
     requests = challenge.request_set.all()
     for r in requests:
         if str(r.tutorName) == str(request.user.username):
             current_request = r
             requested = True
             print(r.confirmed)
             if r.confirmed:
                 hide = False
     if requested:
         return render(request, 'halls/seefiles.html',{'files':files,'requests':requests,'challenge':challenge,'hide':hide,'requested':requested,'current_request':current_request})
     else:
         return render(request,'halls/seefiles.html',{'files':files,'requests':requests,'challenge':challenge,'hide':hide,'requested':requested})
@login_required
def seesolutions(request,pk):
    hidepayment = True
    submitted = False
    r = Request.objects.get(id = pk)
    solutions = r.solution_set.all()
    for s  in solutions:
        if str(s.request.tutorName) == str(request.user.username):
            submitted = True
            print(r.completed)
            if r.completed:
                hidepayment = False
    Arequest = Request.objects.get(id = pk)
    challenge = Arequest.challenge
    solutions = Arequest.solution_set.all()
    return render(request,'halls/seesolutions.html',{'challenge':challenge,'solutions':solutions,'request':Arequest,'hidepayment':hidepayment,'submitted':submitted})

@login_required
def seepayments(request,pk):
    hidepaymentsubmission = True
    payment_submitted = False
    r = Request.objects.get(id = pk)
    payments = r.payment_set.all()
    for p in payments:
        if str(p.request.tutorName) == str(request.user.username):
            payment_submitted = True

            print(r.payment_completed)
            if r.payment_completed:
                hidepaymentsubmission = False
    Arequest = Request.objects.get(id = pk)
    challenge = Arequest.challenge
    payments = Arequest.payment_set.all()
    return render(request,'halls/seepayments.html',{'challenge':challenge,'payments':payments,'request':Arequest,'hidepaymentsubmission':hidepaymentsubmission,'payment_submitted':payment_submitted})

@login_required
@employee_required
def confirmrequest(request,pk):
    r = Request.objects.get(id=pk)
    r.confirmed = True
    r.save()
    messages.success(request,"Request Confirmed Successfully")
    return redirect('allrequests')

@login_required
@tutor_required
def submit_request(request,pk):
    r = Request.objects.get(id=pk)
    r.submitted = True
    print(r.submitted)
    r.save()
    messages.success(request,"Request Submitted Successfully")
    return redirect('dashboard')

@login_required
@employee_required
def reject_submitted_request(request,pk):
    r = Request.objects.get(id=pk)
    r.submitted = False
    print(r.submitted)
    r.save()
    messages.success(request,"Request submission rejected")
    return redirect('allrequests')

@login_required
@employee_required
def reject_confirmed_request(request,pk):
    r = Request.objects.get(id=pk)
    r.confirmed = False
    print(r.confirmed)
    r.save()
    messages.success(request,"Request confirmation rejected")
    return redirect('allrequests')

@login_required
@employee_required
def paymentcompleted(request,pk):
    r = Request.objects.get(id=pk)
    r.payment_completed = True
    print(r.payment_completed)
    r.save()
    messages.success(request,"Payment Completed Successfully")
    return redirect('allrequests')

@login_required
@employee_required
def reject_payment_completed(request,pk):
    r = Request.objects.get(id=pk)
    r.payment_completed = False
    print(r.payment_completed)
    r.save()
    messages.success(request,"Payment Completion Rejected")
    return redirect('allrequests')

@login_required
@employee_required
def completerequest(request,pk):
    r = Request.objects.get(id=pk)
    r.completed = True
    print(r.completed)
    r.save()
    messages.success(request,"Request Solution Accepted, Payment Pending")
    return redirect('allrequests')

@login_required
@employee_required
def reject_completed_request(request,pk):
    r = Request.objects.get(id=pk)
    r.completed = False
    print(r.completed)
    r.save()
    messages.success(request,"Request Completion Rejected")
    return redirect('allrequests')


class EmployeeSignUpView(generic.CreateView):
    model = CustomUser
    form_class = EmployeeSignUpForm
    template_name = 'registration/signup_employee.html'

    def get_context_data(self,**kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        is_employee = True
        is_tutor = False
        return redirect('home')

    def form_valid(self,form):
        user = form.save()
        messages.success(self.request,"Signed Up Successfully")
        login(self.request, user)
        return redirect('home')


class TutorSignUpView(generic.CreateView):
    model = CustomUser
    form_class = TutorSignUpForm
    template_name = 'registration/signup_tutor.html'

    def get_context_data(self,**kwargs):
        kwargs['user_type'] = 'tutor'
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        is_tutor = True
        is_employee = False
        return redirect('create_profile')

    def form_valid(self,form):
        user = form.save()
        messages.success(self.request,"Signed Up Successfully")
        login(self.request, user)
        return redirect('create_profile')

# class SignUp(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('home')
#     template_name = 'registration/signup.html'
#
#     def form_valid(self, form):
#         view = super(SignUp, self).form_valid(form)
#         email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password')
#         user = form.save()
#         login(self.request, user, backend = 'django.contrib.auth.backends.ModelBackend')
#         return view

#CRUD = Create, Read, Update, Destroy
class Login(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        messages.success(self.request,"You are Logged in Successfully")
        return reverse_lazy('home')

@method_decorator([login_required,employee_required], name='dispatch')
class CreateHall(LoginRequiredMixin,generic.CreateView):
    form_class = CreateHallForm
    model =  Hall
    #fields = ['title','image', 'body']
    template_name = 'halls/create_hall.html'
    #success_url = reverse_lazy('edashboard')

    def get_success_url(self):
        s = 'Category '+ self.object.title + ' created successfully'
        messages.success(self.request, s)
        return reverse_lazy('edashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        #super of class is generic CreateView
        super(CreateHall, self).form_valid(form)
        form.save()

        return redirect('edashboard')

class CreateProfile(generic.CreateView):
    form_class = CreateProfileForm
    model = Profile
    template_name = 'halls/create_profile.html'

    def get_success_url(self):
        user = self.object.user
        return reverse_lazy('profilepage',kwargs = {'pk':user.pk })

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.MoneyEarned= 0
        form.instance.Rating = '0'
        super(CreateProfile, self).form_valid(form)
        form.save()
        messages.success(self.request,"Profile Created Successfully")
        return super().form_valid(form)

class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'



@method_decorator([login_required,employee_required], name='dispatch')
class UpdateHall(LoginRequiredMixin,generic.UpdateView):
    model = Hall
    template_name = 'halls/update_hall.html'
    fields = ['title','image','body']
    #success_url = reverse_lazy('edashboard')

    def get_success_url(self):
        s = 'Category '+ self.object.title + ' updated successfully'
        messages.success(self.request,s)
        return reverse_lazy('edashboard')

    def get_object(self):#this does not works with create and detail
        hall = super(UpdateHall, self).get_object()
        return hall

class UpdateProfile(LoginRequiredMixin,generic.UpdateView):
    model = Profile
    template_name = 'halls/update_profile.html'
    form_class=CreateProfileForm

    def get_success_url(self):
        s = 'Profile Updated Successfully'
        messages.success(self.request,s)
        user = self.object.user
        # messages.add_message(self.request,"Profile Updated Successfully")
        return reverse_lazy('profilepage', kwargs = {'pk':user.pk })

    def get_object(self):
        profile = super(UpdateProfile, self).get_object()
        return profile


@method_decorator([login_required,employee_required], name='dispatch')
class DeleteHall(LoginRequiredMixin,generic.UpdateView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    fields = ['title','image','body']
    #success_url = reverse_lazy('edashboard')

    def get_success_url(self):
        s = 'Category '+ self.object.title + ' deleted successfully'
        messages.success(self.request, s)

        return reverse_lazy('edashboard')

    def get_object(self):#this does not works with create and detail
        hall = super(UpdateHall, self).get_object()
        return hall

@method_decorator([login_required,employee_required], name='dispatch')
class AddFile(LoginRequiredMixin,generic.CreateView):
    form_class = AddFileForm
    model =  File
    template_name = 'halls/add_file.html'
    # success_url = "/add_file_completed/"

    def get_success_url(self):

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
        messages.success(self.request,"File Added Successfully")
        return super().form_valid(form)

class AddSolution(LoginRequiredMixin,generic.CreateView):
    form_class = AddSolutionForm
    model =  Solution
    template_name = 'halls/add_solution.html'
    # success_url = "/add_file_completed/"

    def get_success_url(self):

        request = self.object.request
        return reverse_lazy('seesolutions', kwargs = {'pk':request.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.request_id = self.kwargs['pk']
        #super of class is generic CreateView
        super(AddSolution, self).form_valid(form)
        form.save()
        messages.success(self.request,"Solution added Successfully")
        return super().form_valid(form)

@method_decorator([login_required,employee_required], name='dispatch')
class AddPayment(LoginRequiredMixin,generic.CreateView):
    form_class = AddPaymentForm
    model =  Payment
    template_name = 'halls/add_payment.html'
    # success_url = "/add_file_completed/"

    def get_success_url(self):

        request = self.object.request
        return reverse_lazy('seepayments', kwargs = {'pk':request.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.request_id = self.kwargs['pk']
        #super of class is generic CreateView
        super(AddPayment, self).form_valid(form)
        form.save()
        s = 'payment containing ' + self.object.payment_file.url[:40]+'added successfully'
        messages.success(self.request, s)
        return super().form_valid(form)

class RequestChallenge(generic.CreateView):
    form_class = RequestChallengeForm
    model =  Request
    template_name = 'halls/requestchallenge.html'
    # success_url = "/add_file_completed/"

    def get_success_url(self):

        challenge = self.object.challenge
        return reverse_lazy('seefiles', kwargs = {'pk':challenge.pk})

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.challenge_id = self.kwargs['pk']
        form.instance.tutorName = self.request.user.username
        form.instance.tutorId = self.request.user.id
        try:
            user = CustomUser.objects.get(id=form.instance.tutorId)
            profile = Profile.objects.get(user=user)
            form.instance.tutorNumber = profile.WhatsappNumber
        except Profile.DoesNotExist:
            form.instance.tutorNumber = "8541099563"

        #super of class is generic CreateView
        super(RequestChallenge, self).form_valid(form)
        form.save()
        messages.success(self.request,"challenge requested successfully, plz wait till it gets Confirm")
        return super().form_valid(form)

@method_decorator([login_required,employee_required], name='dispatch')
class UpdateFile(LoginRequiredMixin,generic.UpdateView):
    form_class = AddFileForm
    model = File
    template_name = 'halls/update_file.html'
#    fields = ['title','pub_date', 'delete_by','attachment','challenge']
    # success_url = "/update_file_completed/"

    def get_success_url(self):
        s = 'file ' + self.object.title + ' updated successfully'
        messages.success(self.request, s)
        # messages.success(self,"File Updated Successfully")
        challenge = self.object.challenge
        return reverse_lazy('seefiles', kwargs = {'pk':challenge.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        file = super(UpdateFile, self).get_object()
        return file

class UpdateSolution(LoginRequiredMixin,generic.UpdateView):
    form_class = AddSolutionForm
    model = Solution
    template_name = 'halls/update_solution.html'
#    fields = ['title','pub_date', 'delete_by','attachment','challenge']
    # success_url = "/update_file_completed/"

    def get_success_url(self):
        s = 'solution containing ' + self.object.solutionfile.url[23:40] + ' updated successfully'
        messages.success(self.request, s)
        # messages.success(self.request,"Solution Updated Successfully")
        request = self.object.request
        return reverse_lazy('seesolutions', kwargs = {'pk':request.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        solution = super(UpdateSolution, self).get_object()
        return solution

@method_decorator([login_required,employee_required], name='dispatch')
class UpdatePayment(LoginRequiredMixin,generic.UpdateView):
    form_class = AddPaymentForm
    model = Payment
    template_name = 'halls/update_payment.html'
#    fields = ['title','pub_date', 'delete_by','attachment','challenge']
    # success_url = "/update_file_completed/"

    def get_success_url(self):
        s = 'payment containing ' + self.object.payment_file.url[23:40] + ' updated successfully'
        messages.success(self.request, s)
        # messages.success(self.request,"Payment Updated Successfully")
        request = self.object.request
        return reverse_lazy('seepayments', kwargs = {'pk':request.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        payment = super(UpdatePayment, self).get_object()
        return payment


@method_decorator([login_required,employee_required], name='dispatch')
class DeleteFile(LoginRequiredMixin,generic.DeleteView):
    form_class = AddFileForm
    model = File
    template_name = 'halls/delete_file.html'
    #fields = ['title','pub_date', 'delete_by','attachment','challenge']
    def get_success_url(self):
        s = 'file '+ self.object.title +' deleted successfully'
        messages.success(self.request,  s)
        # messages.success(self.request,"File Deleted Successfully")
        challenge = self.object.challenge
        return reverse_lazy('seefiles', kwargs = {'pk':challenge.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        file = super(DeleteFile, self).get_object()
        return file

class DeleteSolution(LoginRequiredMixin,generic.DeleteView):
    form_class = AddSolutionForm
    model = Solution
    template_name = 'halls/delete_solution.html'
    #fields = ['title','pub_date', 'delete_by','attachment','challenge']
    def get_success_url(self):
        s = 'solution containing '+ self.object.solutionfile.url[23:40] +' deleted successfully'
        messages.success(self.request, s)
        # messages.success(self.request,"Solution Deleted Successfully")
        request = self.object.request
        return reverse_lazy('seesolutions', kwargs = {'pk':request.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        solution = super(DeleteSolution, self).get_object()
        return solution

@method_decorator([login_required,employee_required], name='dispatch')
class DeletePayment(LoginRequiredMixin,generic.DeleteView):
    form_class = AddSolutionForm
    model = Solution
    template_name = 'halls/delete_solution.html'
    #fields = ['title','pub_date', 'delete_by','attachment','challenge']
    def get_success_url(self):
        s = 'solution containing '+ self.object.solutionfile.url[23:40] +' deleted successfully'
        messages.success(self.request, s)
        # messages.success(self.request,"Payment Deleted Successfully")
        request = self.object.request
        return reverse_lazy('seesolutions', kwargs = {'pk':request.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        solution = super(DeleteSolution, self).get_object()
        return solution


class DetailFile(LoginRequiredMixin,generic.DetailView):
    model = File
    template_name = 'halls/detail_file.html'

class DetailSolution(LoginRequiredMixin,generic.DetailView):
    model = Solution
    template_name = 'halls/detail_solution.html'


class DetailPayment(LoginRequiredMixin,generic.DetailView):
    model = Payment
    template_name = 'halls/detail_payment.html'
@login_required
@tutor_required
def detail_profile(request, pk):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        return render(request, 'halls/profilepage.html',{'profile':profile})
    except:
        return redirect('create_profile')


@login_required
@employee_required
def see_profile(request,pk):
    user = CustomUser.objects.get(id=pk)
    profile = Profile.objects.get(user=user)
    return render(request,'halls/profilepage.html',{'profile':profile})


class UpdateRequest(LoginRequiredMixin,generic.UpdateView):
    form_class = RequestChallengeForm
    model = Request
    template_name = 'halls/update_request.html'
#    fields = ['title','pub_date', 'delete_by','attachment','challenge']
    # success_url = "/update_file_completed/"

    def get_success_url(self):
        s = 'request by' + self.object.tutorName + ' updated successfully'
        messages.success(self.request, s)
        challenge = self.object.challenge
        # messages.success(self.request,"Request Updated Successfully")
        return reverse_lazy('seefiles', kwargs = {'pk':challenge.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        request = super(UpdateRequest, self).get_object()
        return request

@method_decorator([login_required,employee_required], name='dispatch')
class DeleteRequest(LoginRequiredMixin,generic.DeleteView):
    form_class = RequestChallengeForm
    model = Request
    template_name = 'halls/delete_request.html'
    #fields = ['title','pub_date', 'delete_by','attachment','challenge']
    def get_success_url(self):
        s = 'request by' + self.object.tutorName + ' deleted successfully'
        messages.success(self.request, s)
        challenge = self.object.challenge
        return reverse_lazy('seefiles', kwargs = {'pk':challenge.pk })

    def get_form(self):
        form = super().get_form()
        #form.fields['pub_date'].widget = DateTimePickerInput()
        #form.fields['delete_by'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        request = super(DeleteRequest, self).get_object()
        return request


class DetailRequest(LoginRequiredMixin,generic.DetailView):
    model = Request
    template_name = 'halls/detail_request.html'


@method_decorator([login_required,employee_required], name='dispatch')
class CreateChallenge(LoginRequiredMixin,generic.CreateView):
    form_class = CreateChallengeForm
    model =  Challenge
    template_name = 'halls/create_challenge.html'
    # success_url = "/create_challenge_completed/"

    def get_success_url(self):

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
        s = 'challenge ' + self.object.title + ' created successfully'
        messages.success(self.request, s)
        return super().form_valid(form)


class DetailChallenge(LoginRequiredMixin,generic.DetailView):
    model = Challenge
    template_name = 'halls/detail_challenge.html'

@method_decorator([login_required,employee_required], name='dispatch')
class UpdateChallenge(LoginRequiredMixin,generic.UpdateView):
    form_class = CreateChallengeForm
    model = Challenge
    template_name = 'halls/update_challenge.html'
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body','hall']

    def get_success_url(self):
        s = 'challenge '+ self.object.title + ' updated successfully'
        messages.success(self.request,  s)
        hall = self.object.hall
        return reverse_lazy('seechallenges',kwargs = {'pk':hall.pk })

    def get_form(self):
        form = super().get_form()
        # form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['deadline_date'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        challenge = super(UpdateChallenge, self).get_object()
        # if not challenge.hall.user == self.request.user:
        #     raise Http404
        return challenge

@method_decorator([login_required,employee_required], name='dispatch')
class DeleteChallenge(LoginRequiredMixin,generic.DeleteView):
    form_class = CreateChallengeForm
    model = Challenge
    template_name = 'halls/delete_challenge.html'
    #fields = ['title','url', 'pub_date', 'deadline_date', 'icon', 'body','hall']
    # success_url = "/delete_challenge_completed/"

    def get_success_url(self):
        s = 'challenge '+ self.object.title + ' deleted successfully'
        messages.success(self.request,  s)
        hall = self.object.hall
        return reverse_lazy('seechallenges', kwargs = {'pk':hall.pk })

    def get_form(self):
        form = super().get_form()
        # form.fields['pub_date'].widget = DateTimePickerInput()
        form.fields['deadline_date'].widget = DateTimePickerInput()
        return form

    def get_object(self):
        challenge = super(DeleteChallenge, self).get_object()
        return challenge
