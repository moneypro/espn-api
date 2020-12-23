from espn_api.basketball import Matchup, Team


def get_opponent_team(match_up: Matchup, my_team_id: int) -> Team:
    return match_up.away_team if match_up.home_team.team_id == my_team_id else match_up.home_team


def get_my_team(match_up: Matchup, my_team_id: int) -> Team:
    return match_up.away_team if match_up.home_team.team_id != my_team_id else match_up.home_team
