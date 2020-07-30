from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from .validators import validate_file_extension, validate_file_question, validate_file_solution
class CustomUser(AbstractUser) :
    is_tutor = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=254, unique=True)
    REQUIRED_FIELDS = ['username','is_tutor','is_employee']

    def get_username(self):
        return self.email



class Profile(models.Model):
    User = settings.AUTH_USER_MODEL
    RATING_CHOICES = (
        ('0', 'NotStarted'),
        ('1', 'Poor'),
        ('2','OK'),
        ('3','Nice'),
        ('4','Good'),
        ('5','Excellent')
    )
    FirstName = models.CharField(max_length = 255)
    LastName = models.CharField(max_length = 255)
    Rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    WhatsappNumber = models.CharField(verbose_name="phone number", max_length=10)
    MoneyEarned = models.FloatField()
    Skills = models.TextField()
    email_confirmed = models.BooleanField(default=False)
    University = models.CharField(max_length = 100,blank = True,default="")
    Branch = models.CharField(max_length = 100, blank = True,default="")
    Year = models.IntegerField(blank = True)
    Resume = models.FileField(upload_to='files/resume',blank = True,validators=[validate_file_extension])
    upiId = models.CharField(max_length=255,blank = True,default="")
    AccountNumber = models.CharField(max_length=255,blank=True,default="")
    BeneficiaryName = models.CharField(max_length = 255,blank=True,default="")
    IFSC = models.CharField(max_length = 255,blank=True,default="")
    Other_Details = models.TextField(blank=True,default="")
    def percentRating(self):
        if(self.Rating=='0'):
            return '0%'
        elif(self.Rating=='1'):
            return '20%'
        elif(self.Rating=='2'):
            return '40%'
        elif(self.Rating=='3'):
            return '60%'
        elif(self.Rating=='4'):
            return '80%'
        else:
            return '100%'

    def getFirstName(self):
        return str(FirstName)
    def getLastName(self):
        return str(LastName)

    def getresumeUrl(self):
        if self.Resume:
            return self.Resume.url
        else:
            return ''


class Hall(models.Model):
    User = settings.AUTH_USER_MODEL
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:500]




class Challenge(models.Model):
    TYPE_CHOICES = (
        ('P', 'Project'),
        ('A', 'Assignment'),
        ('T','Time_Bound_Challenges')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now=True)

    deadline_date = models.DateTimeField()
    body = models.TextField()
    stipend = models.FloatField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def get_challenge_id(self):
        return self.title
    def get_absolute_url(self):
        return reverse('seechallenges', kwargs = {'pk': self.hall.pk})

    def get_Type(self):
        if(self.type=='P'):
             return 'Project'
        elif(self.type=='A'):
             return 'Assignment'
        else:
             return 'Time_Bound_Challenge'
    def timeleft(self):
        return self.deadline_date - timezone.now()

    def get_time_left(self):
        left = self.timeleft()
        time = int(left.total_seconds())
        if(time <=0):
            return 0
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        s = ""
        if(day!=0):
            s = "("+str(day)+"d:"
        if(hour!=0):
            if(day==0):
                s = s+"("
            s = s+str(hour)+"hr:"
        if(minutes!=0):
            if(day==0 and hour==0):
                s = s+ "("
            s = s+str(minutes)+"min:"
        if(seconds!=0):
            if(day==0 and hour==0 and minutes==0):
                s = s+ "("
            s = s+str(seconds)+"sec)"
        return s;
    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub.date.strftime('%b %e %Y')


class Request(models.Model):
    tutorName = models.CharField(max_length = 255)
    HowToSolve = models.TextField()
    tutorId = models.IntegerField()
    tutorNumber = models.CharField(verbose_name="phone number", max_length=10)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True)
    submitted = models.BooleanField(default = False)
    confirmed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    payment_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.tutorName

    def whatsapp(self):
        print(self.tutorNumber)
        return ("https://wa.me"+"/91"+str(self.tutorNumber))

    def whatsapp2(self):
        return ("https://wa.me"+"/918541099563")

class Payment(models.Model):
    payment_details = models.TextField()
    payment_file = models.FileField(upload_to='files/payments',blank='True', validators=[validate_file_extension])
    request = models.ForeignKey(Request,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.ans

    def paymentshorturl(self):
        return self.payment_file.url[23:40]

    def get_absolute_url(self):
        return reverse('seefiles', kwargs = {'pk': self.request.challenge.pk})

class Solution(models.Model):
     ans = models.TextField()
     solutionfile = models.FileField(upload_to='files/solutions',blank='True', validators=[validate_file_solution])
     request = models.ForeignKey(Request,on_delete=models.SET_NULL,null=True)

     def __str__(self):
         return self.ans

     def solutionshorturl(self):
         return self.solutionfile.url[23:40]

     def get_absolute_url(self):
         return reverse('seefiles', kwargs = {'pk': self.request.challenge.pk})



class File(models.Model):
    title = models.CharField(max_length=255)
    #pub_date = models.DateTimeField()
    #description = models.TextField()
    #delete_by = models.DateTimeField()
    attachment = models.FileField(upload_to='files/',validators=[validate_file_question])
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('seefiles', kwargs = {'pk': self.challenge.pk})

    def pub_date_pretty(self):
        return self.pub.date.strftime('%b %e %Y')

    def substr(self):
        return self.attachment.url[13:]
