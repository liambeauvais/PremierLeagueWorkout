from django.db import models


# Create your models here.
from championship.models import Championship


class Team(models.Model):
    name = models.CharField(null=False, blank=False, unique=True)
