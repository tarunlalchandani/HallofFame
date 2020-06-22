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
    url = models.URLField()
    pub_date = models.DateTimeField()
    deadline_date = models.DateTimeField()
    icon = models.ImageField(upload_to='images/')
    body = models.TextField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub.date.strftime('%b %e %Y')

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
