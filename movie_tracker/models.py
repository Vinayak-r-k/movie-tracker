from django.db import models
class Details(models.Model):
    title = models.CharField(max_length=300)
    overview = models.CharField(max_length=500)

# Create your models here.
