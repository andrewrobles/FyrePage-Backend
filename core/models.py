from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=30)
    url = models.CharField(max_length=30)