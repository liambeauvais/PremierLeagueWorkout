from django.db import models

# Create your models here.
from championship.models import Championship
from team.models import Team


class Match(models.Model):
    championship = models.ForeignKey(
        Championship,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="matches"
    )
    date = models.DateField(null=False, blank=False)
    week = models.PositiveIntegerField(null=False, blank=False)
    home = models.ForeignKey(
        Team,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="home_matches"
    )
    away = models.ForeignKey(
        Team,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="away_matches"
    )
    home_goals = models.PositiveIntegerField(null=False, blank=False)
    away_goals = models.PositiveIntegerField(null=False, blank=False)
    winner = models.ForeignKey(
        Team,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        default=None,
        related_name="won_matches"
    )
