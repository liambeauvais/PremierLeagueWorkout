import os
from datetime import datetime

import pandas as pd

from championship.models import Championship
from team.models import Team
from team_championship_stats.models import TeamChampionshipStats


def transform_league_tables() -> str:
    is_already_done: bool = len(Championship.objects.filter(name="Premier League")) > 0
    if is_already_done:
        return "Already Done"
    df: pd.DataFrame = pd.read_csv(f'{os.environ.get("ABSOLUTE_PATH")}/data/premier-league-tables.csv')
    first_year: int = 1993
    while first_year <= datetime.now().year:
        championship: Championship = Championship.objects.create(
            league_year=first_year,
            name="Premier League"
        )
        championship.save()
        print(championship)

        for index, row in df.iterrows():
            if row['Season_End_Year'] == first_year:
                team: list[Team] = Team.objects.filter(name=row['Team']).all()
                if not len(team) > 0:
                    team: Team = Team.objects.create(
                        name=row['Team'],
                    )
                    team.save()
                else:
                    team: Team = team[0]

                TeamChampionshipStats.objects.create(
                    championship_id=championship.id,
                    team_id=team.id,
                    league_points=row['Pts'],
                    losses=row['L'],
                    goals_for=row['GF'],
                    matches_played=row['MP'],
                    goals_against=row['GA'],
                    goal_difference=row['GD'],
                    draws=row['D'],
                    rank=row['Rk'],
                    wins=row['W'],
                )

        first_year += 1
    return "OK"
