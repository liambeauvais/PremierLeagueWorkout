import os
from datetime import datetime

import pandas as pd

from championship.models import Championship
from match.models import Match
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


def transform_league_matches():
    matches_done = len(Match.objects.filter(championship__name="Premier League").all()) > 0
    if matches_done:
        return "Already Done"

    df = pd.read_csv(f'{os.environ.get("ABSOLUTE_PATH")}/data/premier-league-matches.csv')
    first_year: int = 1993

    while first_year <= datetime.now().year:
        championship: Championship = Championship.objects.filter(
            league_year=first_year,
            name="Premier League"
        )[0]
        for index, row in df.iterrows():
            league_year = row['Season_End_Year']
            if league_year == first_year:
                home: Team = Team.objects.filter(
                    name=row['Home']
                ).all()[0]

                away: Team = Team.objects.filter(
                    name=row['Away']
                ).all()[0]

                winner_filter = row['Home'] \
                    if row['FTR'] == "H" \
                    else row['Away'] \
                    if row['FTR'] == 'A' \
                    else None
                winner: Team = Team.objects.filter(
                    name=winner_filter
                ).all()[0] if winner_filter is not None else None

                Match.objects.create(
                    championship_id=championship.id,
                    home_id=home.id,
                    away_id=away.id,
                    date=datetime.strptime(row['Date'], '%Y-%m-%d'),
                    week=row['Wk'],
                    away_goals=row['AwayGoals'],
                    home_goals=row['HomeGoals'],
                    winner=winner
                )
        first_year += 1

    return "OK"
