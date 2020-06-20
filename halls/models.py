from django.db import models
from django.contrib.auth.models import User

class Hall(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete = models.CASCADE)


class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length = 255)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def form_valid(self, form):
        form.instance.user = self.request.user
        #super of class is generic CreateView
        super(CreateHall, self).form_valid(form)
