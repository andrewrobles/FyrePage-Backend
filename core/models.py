from django.db import models

# Create your models here.
class Link(models.Model):
    text = models.CharField(max_length=30)
    url = models.CharField(max_length=30)