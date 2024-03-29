# Create your views here.
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd

from team.models import Team
from team_championship_stats.models import TeamChampionshipStats


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class GoalsSerializer(serializers.ModelSerializer):
    championship_year = serializers.CharField(source='championship.league_year')
    team = TeamSerializer()

    class Meta:
        model = TeamChampionshipStats
        exclude = ['championship']
        include = ['championship_year', 'team']


class TeamChampionshipStatsSerializer(serializers.ModelSerializer):
    championship = serializers.CharField(source="championship.league_year")

    class Meta:
        model = TeamChampionshipStats
        exclude = ['id']


class TeamChampionshipStatsViewset(viewsets.ModelViewSet):
    queryset = TeamChampionshipStats.objects.all()
    serializer_class = TeamChampionshipStatsSerializer

    @action(methods=['GET'], detail=False)
    def winners_count(self, request):
        queryset: list[TeamChampionshipStats] = self.get_queryset()
        winning_teams = Team.objects.filter(
            id__in=[team.team_id for team in queryset if team.rank == 1]
        ).distinct().all()
        winning_teams_count = winning_teams.count()
        serializer = TeamSerializer(winning_teams, many=True)
        return Response(
            {
                "winning_teams": serializer.data,
                "count": winning_teams_count
            }
        )

    @action(methods=['GET'], detail=False)
    def goals_by_year(self, request):
        queryset = self.get_queryset()
        serializer = GoalsSerializer(queryset, many=True)
        df = pd.DataFrame(data=serializer.data)
        df = df.drop(
            columns=['team']
        )
        goal_count: pd.DataFrame = df.groupby('championship_year').mean()
        response = {}
        for index, row in goal_count.iterrows():
            response[index] = row['goals_for']

        return Response(response)

    @action(methods=['GET'], detail=False)
    def winners(self, request):
        queryset: list[TeamChampionshipStats] = self.get_queryset()
        winners: list[TeamChampionshipStats] = [
            championship_stats for championship_stats in queryset
            if championship_stats.rank == 1
        ]

        serializer = GoalsSerializer(winners, many=True)
        return Response(
            {
                championship_stats['championship_year']: {
                    "team": championship_stats['team'],
                    "goals_for": championship_stats['goals_for'],
                    "goals_against": championship_stats['goals_against']
                }
            } for championship_stats in serializer.data
        )
