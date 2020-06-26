from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



class CustomUser(AbstractUser) :

    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=254, unique=True)
    REQUIRED_FIELDS = ['username']

    def get_username(self):
        return self.email

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
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    deadline_date = models.DateTimeField()
    icon = models.ImageField(upload_to='images/')
    body = models.TextField()
    stipend = models.FloatField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub.date.strftime('%b %e %Y')

class File(models.Model):
    title = models.CharField(max_length=255)
    #pub_date = models.DateTimeField()
    #description = models.TextField()
    #delete_by = models.DateTimeField()
    attachment = models.FileField(upload_to='files/')
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def pub_date_pretty(self):
        return self.pub.date.strftime('%b %e %Y')

    def substr(self):
        return self.attachment.url[13:]
