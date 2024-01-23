from django.db import models

# Create your models here.
from championship.models import Championship
from team.models import Team


class TeamChampionshipStats(models.Model):
    championship = models.ForeignKey(
        Championship,
        null=False,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="championship_stats"
    )
    team = models.ForeignKey(
        Team,
        null=False,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="championship_stats"
    )
    rank = models.PositiveIntegerField(null=False, blank=False)
    matches_played = models.PositiveIntegerField(null=False, blank=False)
    wins = models.PositiveIntegerField(null=False, blank=False)
    draws = models.PositiveIntegerField(null=False, blank=False)
    losses = models.PositiveIntegerField(null=False, blank=False)
    goals_for = models.PositiveIntegerField(null=False, blank=False)
    goals_against = models.PositiveIntegerField(null=False, blank=False)
    goal_difference = models.IntegerField(null=False, blank=False)
    league_points = models.IntegerField(null=False, blank=False)

