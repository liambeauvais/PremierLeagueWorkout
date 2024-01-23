from django.db import models


# Create your models here.

class Championship(models.Model):
    name = models.CharField(null=False, blank=False)
    league_year = models.CharField(null=False, blank=False)
