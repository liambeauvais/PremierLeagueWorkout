# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from team.models import Team
from team_championship_stats.views import TeamSerializer


def get_best_team(most_won_matches: list[dict], targeted_key: str) -> dict:
    best_team = {
        'team': {},
        'won_matches': 0,
        'titles': 0
    }
    for team in most_won_matches:
        if team[targeted_key] > best_team[targeted_key]:
            best_team = team

    return best_team


class TeamViewset(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(methods=['GET'], detail=False)
    def most_won_matches(self, request):
        queryset: list[Team] = self.get_queryset()
        most_won_matches: list[dict] = [
            {
                "team": {
                    "id": team.id,
                    "name": team.name
                },
                "won_matches": sum(
                    [championship_stats.wins
                     for championship_stats in team.championship_stats.all()]
                ),
                "titles": sum(
                    [championship_stats.rank
                     for championship_stats in team.championship_stats.all()
                     if championship_stats.rank == 1]
                )
            }
            for team in queryset
        ]

        best_team: dict[str, dict or int] = get_best_team(most_won_matches, 'won_matches')
        best_team_on_titles: dict[str, dict or int] = get_best_team(most_won_matches, 'titles')

        return Response(
            {
                'best_team_on_matches': best_team,
                'best_team_on_titles': best_team_on_titles
            }
        )

    @action(methods=['GET'], detail=False)
    def teams_longevity(self, request):
        queryset: list[Team] = self.get_queryset()
        teams= [
            {
                "id": team.id,
                "name": team.name,
                "longevity_in_years":team.championship_stats.count()
            } for team in queryset
        ]
        teams = sorted(
            teams,
            key=lambda x: x['longevity_in_years'],
            reverse=True
        )
        return Response(teams)

